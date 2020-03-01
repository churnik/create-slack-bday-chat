from flask import Response, jsonify, make_response
from loguru import logger
from slack.errors import SlackApiError

from .errors import *
from .main import app


@app.errorhandler(BaseAppException)
def app_error_handler(e: BaseAppException):
    return make_response(jsonify(e.to_dict()), e.error_code)


@app.errorhandler(SlackApiError)
def handle_slack_error(e: SlackApiError):
    resp = e.response

    if resp.get("error") == "name_taken":
        return {"response_type": "in_channel", "text": "Channel already exists."}
    else:
        raise e


@app.errorhandler(Exception)
def exception(e: Exception) -> Response:
    logger.exception("Unexpected error occurred. {}", e)
    return make_response(
        jsonify(
            {
                "error": "unexpected",
                "params": {
                    "message": str(e).replace("\n", " ") + str(getattr(e, "original_exception", ""))
                },
            }
        ),
        500,
    )
