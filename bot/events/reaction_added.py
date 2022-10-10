import re
from bot import bot
from bot.utils import ts_to_date, get_delete_reason
from bot.utils.get_user import get_user
from bot.utils.slack_messages import delete_message
from bot.config import admins, channels, DANGER_REACTIONS_REGEX, PROFILE_LINK_REGEX
from bot.database.sheets import sheet


async def filter_messages(context) -> bool:
    message = context.get('message')

    if message is None:
        return False

    return 'pinned_to' not in message and 'subtype' not in message


@bot.event('reaction_added', matchers=[filter_messages])
async def handle_reaction_added_event(event, context):
    reaction = event['reaction']
    user = context['user_data']
    user_id = user['id']
    channel = event['item']['channel']
    message_ts = event['item']['ts']
    event_ts = event['event_ts']

    message = context['message']


    if reaction == 'test_tube' and user_id in admins:
        await delete_message(channel_id=channel, ts=message_ts)
        return

    # Danger reactions are used to delete messages
    if not re.search(DANGER_REACTIONS_REGEX, reaction):
        return

    if channel == channels['ANTISPAMERS'] and 'bot_profile' in message:
        await delete_message(channel_id=channel, ts=message_ts)

        blocks = message['blocks']
        user_id = re.search(r"(?<=<@)[A-Z0-9]*", blocks[2]['elements'][0]['text']).group()
        task_link = re.search(r"https.+(?=>)", blocks[0]['text']['text']).group()
        sender = await get_user(user_id)

        sheet.worksheet('Принятые репорты').insert_row([
            task_link,
            sender['nick'],
            context['user_nick'],
            ts_to_date(event_ts)
        ], 2)
    elif channel == channels['HELP']:
        await delete_message(channel_id=channel, ts=message_ts)

        sheet.worksheet('#help').insert_row([
            ts_to_date(message_ts),
            context['message_user_nick'],
            message['text'],
            context['user_nick'],
            ts_to_date(event_ts)
        ], 2)
    elif channel == channels['TO_DELETE'] and event['user'] in admins:
        await delete_message(channel_id=channel, ts=message_ts)

        message_text = message['text']

        profile_link = re.search(PROFILE_LINK_REGEX, message_text)
        delete_reason = get_delete_reason(message_text)

        sheet.worksheet('#to-delete').insert_row([
            delete_reason,
            profile_link.group() if profile_link else '?',
            context['message_user_nick'],
            ts_to_date(message_ts),
            ts_to_date(event_ts),
            message_text
        ], 2)
    elif channel == channels['MODERATORS']:
        await delete_message(channel_id=channel, ts=message_ts)
