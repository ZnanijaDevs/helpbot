import re
from bot import bot
from bot.config import channels
from bot.utils.get_question import get_question
from bot.utils.slack_messages import delete_message
from bot.utils import find_task_id


@bot.message(re.compile(r"снять\s(отметку|нарушение)|:blue_approve:", re.IGNORECASE))
async def send_to_antispamers(message):
    task_id = find_task_id(message['text'])
    if task_id is None:
        return

    question_data = get_question(task_id)
    if question_data is None:
        return

    question = question_data['task']

    message_blocks = [{
        'type': 'section',
        'text': {
            'type': 'mrkdwn',
            'text': f":lower_left_ballpoint_pen: *{question.get('subject', '')}* *{question['link']}*"
        }
    }, {
        'type': 'section',
        'text': {
            'type': 'mrkdwn',
            'text': question['content']['short']
        }
    }, {
		'type': 'context',
		'elements': [{
			'type': 'mrkdwn',
			'text': f"Отправлено <@{message['user']}>\n{message['text']}"
		}]
    }]

    await bot.client.chat_postMessage(
        channel=channels['ANTISPAMERS'],
        blocks=message_blocks,
        text='Снятие отметки нарушения'
    )

    await delete_message(channel_id=message['channel'], ts=message['ts'])
