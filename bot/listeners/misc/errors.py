import os
from slack_bolt.response import BoltResponse
from slack_bolt.error import BoltUnhandledRequestError
from bot import bot


@bot.error
async def error_handler(error, logger):
    if isinstance(error, BoltUnhandledRequestError):
        return BoltResponse(status=202, body="")

    if os.environ['MODE'] == 'production':
        logger.exception(f"Error: {error}")
    else:
        print(f"An error occured: {error}")

    return BoltResponse(status=500, body="Error")
