import logging
from sentry_sdk import capture_exception
from slack_bolt.response import BoltResponse
from slack_bolt.error import BoltUnhandledRequestError
from bot import bot
from getenv import env


@bot.error
async def error_handler(error: Exception):
    if isinstance(error, BoltUnhandledRequestError):
        return BoltResponse(status=202, body='')

    if env('MODE') == 'production':
        capture_exception(error)
    else:
        logging.exception(error)

    return BoltResponse(status=500, body='Internal server error')
