from dataclasses import dataclass
from typing import List, Optional, Tuple

from slack import WebClient

from create_slack_bday_chat.errors import WrongNumberOfArgumentsException


@dataclass
class ChannelInfo:
    channel_id: str
    channel_name: str


@dataclass
class UserInfo:
    user_id: str
    user_name: str


class SlackCreateCommandArgumentsParser:
    @staticmethod
    def get_id_and_name(data: str):
        d_id, d_name = data.strip("<>").split("|")

        return d_id.strip("#@"), d_name.strip("#@")

    def parse(self, args: Optional[str]) -> Tuple[ChannelInfo, UserInfo, Optional[str]]:
        if args is None:
            raise WrongNumberOfArgumentsException()

        split_args: List[str] = args.split(" ")

        if 2 <= len(split_args) <= 3:
            (channel_id, channel_name), (user_id, user_name) = map(
                self.get_id_and_name, split_args[:2]
            )
            channel = ChannelInfo(channel_id, channel_name)
            user = UserInfo(user_id, user_name)

            if len(split_args) == 2:
                return channel, user, None
            else:
                return channel, user, split_args[2]

        else:
            raise WrongNumberOfArgumentsException()


class SlackUpdateCommandArgumentsParser(SlackCreateCommandArgumentsParser):
    def parse(self, args: Optional[str]) -> Tuple[ChannelInfo, UserInfo, ChannelInfo]:
        if args is None:
            raise WrongNumberOfArgumentsException()

        split_args: List[str] = args.split(" ")

        if len(split_args) == 3:
            (
                (channel_id, channel_name),
                (user_id, user_name),
                (update_channel_id, update_channel_name),
            ) = map(self.get_id_and_name, split_args)
            channel = ChannelInfo(channel_id, channel_name)
            user = UserInfo(user_id, user_name)
            update_channel = ChannelInfo(update_channel_id, update_channel_name)

            return channel, user, update_channel

        else:
            raise WrongNumberOfArgumentsException()


class IterAllUsers:
    def __init__(self, slack_client: WebClient):
        self.slack_client = slack_client

    def iterate(self, channel: ChannelInfo, cursor: Optional[str] = None):
        if cursor is not None:
            data = self.slack_client.conversations_members(
                channel=channel.channel_id, cursor=cursor
            )
        else:
            data = self.slack_client.conversations_members(channel=channel.channel_id)
        user_ids = data["members"]

        for u_id in user_ids:
            yield u_id

        cursor = data["response_metadata"]["next_cursor"]
        if data["response_metadata"]["next_cursor"] != "":
            for u_id in self.iterate(channel, cursor):
                yield u_id
