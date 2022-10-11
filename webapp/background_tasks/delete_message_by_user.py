import logging
from slack_sdk.errors import SlackApiError
from bot import bot
from bot.database import redis
from bot.config import channels
from getenv import env


async def delete_message_by_user(user_id: int):
    """Delete message in #to-delete by user ID"""
    key_matches = redis.keys(f"todelete:{user_id}:**")

    if len(key_matches) == 0:
        return

    for key in key_matches:
        ts = key.decode('utf-8').split(':')[2]

        try:
            await bot.client.reactions_add(
                token=env('SLACK_USER_TOKEN'),
                channel=channels['TO_DELETE'],
                name='magic_wand',
                timestamp=ts,
            )
        except SlackApiError as exc:
            logging.error(
                'Failed to add a reaction to a message with ts %s: %s',
                ts,
                str(exc)
            )
