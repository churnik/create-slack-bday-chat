import logging
import sys
import uuid
from datetime import datetime

from flask import Flask, Response, g, request
from loguru import logger
from slack import WebClient

from create_slack_bday_chat.parser import (IterAllUsers, SlackCreateCommandArgumentsParser,
                                           SlackUpdateCommandArgumentsParser)
from .log import DevelopFormatter, JsonSink

app = Flask(__name__)
app.config.from_envvar("CREATE_SLACK_BDAY_CHAT_FLASK_CONFIG")

COMPONENT_NAME = "create-slack-bday-chat-back"

logger.remove()
if app.config["FLASK_ENV"] == "development":
    develop_fmt = DevelopFormatter(COMPONENT_NAME)
    logger.add(sys.stdout, format=develop_fmt)
else:
    json_sink = JsonSink(COMPONENT_NAME)
    logger.add(json_sink)

logger.configure(
    patcher=lambda record: record["extra"].update(correlation_id=getattr(g, "correlation_id", None))
)
app.logger.disabled = True
logging.getLogger("werkzeug").disabled = True


@app.after_request
def after_request_func(response: Response):
    logger.bind(
        status_code=response.status_code,
        request_path=g.request_path,
        received_at=g.received_at,
        remote_address=g.remote_address,
    ).info("Request ended with {}", response.status_code)
    return response


@app.before_request
def before_request_func():
    g.correlation_id = str(uuid.uuid4())
    g.request_path = request.path
    g.received_at = datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")
    g.remote_address = request.remote_addr


# Now you can do some setup using `@app.before_first_request()`. Database connection for example.


@app.before_first_request
def setup_slack_client():
    app.slack_client = WebClient(token=app.config["SLACK_BOT_TOKEN"])
    app.iter_all_users = IterAllUsers(app.slack_client)


@app.before_first_request
def setup_parsers():
    app.create_args_parser = SlackCreateCommandArgumentsParser()
    app.update_args_parser = SlackUpdateCommandArgumentsParser()
