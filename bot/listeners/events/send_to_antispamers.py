import re
from bot import bot
from bot.config import TASK_ID_REGEX, channels
from bot.utils.brainly_graphql import client, to_base64
from bot.utils.slack_messages import delete_message


@bot.message(re.compile(r"снять\s(отметку|нарушение)|:blue_approve:", re.IGNORECASE))
async def send_to_antispamers(message, logger):
    task_id = re.search(TASK_ID_REGEX, message['text'])
    if task_id is None:
        return

    task_id = task_id.group()

    question_data = await client.execute_async(query="""
        query GetQuestion($questionId: ID!) {
            question(id: $questionId) {
                subject {name}
                content
                answers { nodes {content} }
            }
        }
    """, variables={
        'questionId': to_base64(task_id, 'question')
    })

    if "errors" in question_data:
        logger.error(f"An error has occured while trying to fetch Brainly: {question_data}")
        return

    question = question_data['data']['question']

    if question is None:
        logger.error(f"The question {task_id} does not exist")
        return

    question_content = re.sub(r"<\w+\s?\/?>", '', question['content'])
    subject = question['subject']['name']
    answers_count = len(question['answers']['nodes'])

    message_blocks = [{
        'type': 'section',
        'text': {
            'type': 'mrkdwn',
            'text': f":lower_left_ballpoint_pen: [*{subject}*, ответы: *{answers_count}*] *<https://znanija.com/task/{task_id}>*"
        }
    }, {
        'type': 'section',
        'text': {
            'type': 'mrkdwn',
            'text': f"{question_content[:300]}..." if len(question_content) > 300 else question_content
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
