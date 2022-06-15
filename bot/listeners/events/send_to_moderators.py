import re
from bot import bot
from bot.config import channels
from bot.utils.slack_messages import delete_message
from bot.utils import find_task_id
from bot.utils.brainly_graphql import get_question


@bot.message(re.compile(r"на исправление", re.IGNORECASE))
async def send_to_moderators(message):
    task_id = find_task_id(message['text'])
    reason = re.search(r"(?<=\()[^)]+", message['text'], re.IGNORECASE)

    if task_id is None or reason is None:
        return

    question = await get_question(task_id)

    subject = question['subject']['name']
    answers_count = question['answers_count']
    reason = reason.group().strip()

    await bot.client.chat_postMessage(
        channel=channels['MODERATORS'],
        blocks=[{
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': f"*{subject}, ответы: {answers_count}* <https://znanija.com/task/{task_id}> {reason}\n{question['short_content']}"
            }
        }, {
            'type': 'context',
            'elements': [{
                'type': 'mrkdwn',
                'text': f"<@{message['user']}>"
            }]
        }],
        text='На исправление!'
    )

    await delete_message(channel_id=message['channel'], ts=message['ts'])
