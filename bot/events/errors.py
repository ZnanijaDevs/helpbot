from sentry_sdk import capture_exception
from slack_bolt.response import BoltResponse
from slack_bolt.error import BoltUnhandledRequestError
from bot import bot


@bot.error
async def error_handler(error):
    if isinstance(error, BoltUnhandledRequestError):
        return BoltResponse(status=202, body="")

    capture_exception(error)

    return BoltResponse(status=500, body="Error")
