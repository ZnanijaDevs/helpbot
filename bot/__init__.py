import logging
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler


logging.basicConfig(filename='logger.log', filemode='w')

bot = AsyncApp(
    name='helpbot',
    raise_error_for_unhandled_request=True
)

events_handler = AsyncSlackRequestHandler(bot)
