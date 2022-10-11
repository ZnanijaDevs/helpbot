import re
from slackblocks import Message, SectionBlock, ContextBlock, Text
from bot import bot
from bot.config import channels
from bot.utils.get_question import get_question
from bot.utils.slack_messages import delete_message
from bot.utils import find_task_id


@bot.message(re.compile(r"снять\s(отметку|нарушение)|:blue_approve:", re.IGNORECASE))
async def send_to_antispamers(message, context):
    task_id = find_task_id(message['text'])
    if task_id is None:
        return

    question_data = get_question(task_id)
    if question_data is None:
        return

    question = question_data['task']

    await bot.client.chat_postMessage(**Message(
        text=f"{context['user_nick']} {question['link']} - снять нарушение!",
        channel=channels['ANTISPAMERS'],
        blocks=[
            SectionBlock(f":lower_left_ballpoint_pen: {question.get('subject', '')} {question['link']}"),
            SectionBlock(question['content']['short'] or '-'),
            ContextBlock(Text(f"{message['text']}\nОтправлено <@{message['user']}>")),
        ]
    ))

    await delete_message(channel_id=message['channel'], ts=message['ts'])
