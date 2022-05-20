from bot import bot
from bot.utils.get_user import get_user


@bot.use
async def get_extra_info(context, payload, next):
    if 'user' in payload:
        slack_user = await get_user(payload['user'])

        context['user_data'] = slack_user
        context['user_nick'] = slack_user['nick']


    if payload['type'] == 'reaction_added':
        item_ts = payload['item']['ts']

        messages = await bot.client.conversations_history(
            limit=1,
            channel=payload['item']['channel'],
            inclusive=True,
            latest=item_ts
        )

        for message in messages['messages']:
            if message['ts'] == item_ts:
                context['message'] = message

                author = await get_user(message['user'])
                context['message_user'] = author
                context['message_user_nick'] = author['nick']


    await next()
