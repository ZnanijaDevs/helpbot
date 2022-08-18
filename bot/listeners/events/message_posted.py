import re
from bot import bot
from bot.config import PROFILE_LINK_REGEX
from bot.utils import get_delete_reason
from bot.database import redis


@bot.message(re.compile(PROFILE_LINK_REGEX))
async def save_message(message, logger):
    profile_link = re.search(PROFILE_LINK_REGEX, message['text'])

    if profile_link is None:
        logger.info(f"Failed to find the profile link in the message: {message['text']}")
        return

    profile_link = profile_link.group()
    user_id = profile_link.split('-')[-1]

    # Save message data in the Redis storage
    redis.set(
        f"todelete:{user_id}:{message['ts']}:{message['user']}",
        get_delete_reason(message['text'])
    )
