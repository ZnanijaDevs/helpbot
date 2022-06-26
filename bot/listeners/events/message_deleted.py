import re
from bot import bot
from bot.database import redis
from bot.config import channels, PROFILE_LINK_REGEX
from bot.utils import get_delete_reason


async def filter_messages(event):
    if event.get('subtype') != 'message_deleted' or event['channel'] != channels['TO_DELETE']:
        return

    return get_delete_reason(event['previous_message']['text']) != ''


@bot.event(event='message', matchers=[filter_messages])
async def handle_message_deleted_event(event, logger):
    previous_message = event['previous_message']
    message_text = previous_message['text']

    # Find user ID
    profile_link = re.search(PROFILE_LINK_REGEX, message_text)
    if profile_link is None:
        logger.info(f"Profile link not found: {message_text}")
        return

    user_id = profile_link.group().split('-')[-1]

    redis.delete(
        f"todelete:{user_id}:{previous_message['ts']}:{previous_message['user']}"
    )
