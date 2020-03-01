from flask import Blueprint, Response, make_response, request
from loguru import logger
from slack import WebClient

from create_slack_bday_chat.errors import UnauthorizedException
from create_slack_bday_chat.parser import ChannelInfo, UserInfo
from .main import app

app_bp = Blueprint("version_blueprint", __name__)


@app_bp.route("/ping")
def ping() -> Response:
    logger.info("Got ping request!")
    return make_response("pong")


def generate_channel_name(user: UserInfo):
    return f"bday_{user.user_name}_{user.user_id}"[:80]


@app_bp.route("/slack/create", methods=["POST"])
def create():

    if request.form["token"] != app.config["SLACK_VERIFICATION_TOKEN"]:
        raise UnauthorizedException()

    slack_client: WebClient = app.slack_client

    channel: ChannelInfo
    user: UserInfo
    channel, user, channel_name = app.create_args_parser.parse(request.form.get("text"))

    logger.info(
        "Creating new group without {} from channel {}", user.user_name, channel.channel_name
    )

    if channel_name is None:
        channel_name = generate_channel_name(user)
    resp = slack_client.channels_create(name=channel_name)
    group_id = resp.get("channel", {}).get("id")
    logger.info("Creating channel {} with id {}", channel_name, group_id)

    logger.info("Inviting users")
    for member in app.iter_all_users.iterate(channel):
        if member != user.user_id:
            slack_client.channels_invite(channel=group_id, user=member)

    return {"response_type": "in_channel", "text": f"Created channel {channel_name}"}, 200


app.register_blueprint(app_bp, url_prefix="/v0/")
