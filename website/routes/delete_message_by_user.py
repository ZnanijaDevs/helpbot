import os
from fastapi import status, Response
from pydantic import conint
from bot import bot
from bot.config import channels
from bot.database import redis
from website.app import app


@app.post('/delete_user/{user_id}')
async def delete_message_by_user(user_id: conint(gt=3)):
    matches = redis.keys(f"todelete:{user_id}:**")

    if len(matches) == 0:
        return 'Message not found'

    for match in matches:
        ts = str(match).split(':')[2]

        redis.delete(match)

        await bot.client.reactions_add(
            token=os.environ['SLACK_USER_TOKEN'],
            channel=channels['TO_DELETE'],
            name='canc_noj',
            timestamp=ts
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
