from time import time
import re
from bot import bot
from bot.config import channels
from bot.utils.slack_messages import delete_message
from bot.utils import find_task_id, ts_to_date
from bot.utils.get_question import get_question
from bot.database.sheets import sheet


@bot.message(re.compile(r"на исправление", re.IGNORECASE))
async def send_to_moderators(message, context):
    task_id = find_task_id(message['text'])
    reason = re.search(r"(?<=\()[^)]+", message['text'], re.IGNORECASE)

    if task_id is None or reason is None:
        return

    question = get_question(task_id)

    if question is None:
        return

    subject = question['subject']
    answers_count = question['answers_count']
    reason = reason.group().strip()

    await bot.client.chat_postMessage(
        channel=channels['MODERATORS'],
        blocks=[{
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': f"*{subject}, ответы: {answers_count}* <{question['link']}>\n{reason}"
            }
        }, {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': question['short_content']
            }
        }, {
		    'type': 'context',
		    'elements': [{
			    'type': 'mrkdwn',
			    'text': f"Отправлено <@{message['user']}>"
		    }]
        }],
        text='На исправление!'
    )

    await delete_message(channel_id=message['channel'], ts=message['ts'])

    sheet.worksheet('Отправленные на исправление - Лог').insert_row([
        ts_to_date(time()),
        context['user_nick'],
        question['link'],
        subject,
        reason,
        message['text']
    ], 2)
