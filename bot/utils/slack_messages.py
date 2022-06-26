import os
from bot import bot


async def delete_message(channel_id: str, ts: str, clear_threads: bool | None = True):
    """ Deletes a message in Slack. """
    if clear_threads:
        replies = await bot.client.conversations_replies(channel=channel_id, ts=ts)
        for reply in replies['messages']:
            if 'parent_user_id' not in reply:
                continue

            await bot.client.chat_delete(
                token=os.environ['SLACK_ADMIN_TOKEN'],
                ts=reply['ts'],
                channel=channel_id
            )

    await bot.client.chat_delete(
        channel=channel_id,
        ts=ts,
        token=os.environ['SLACK_ADMIN_TOKEN']
    )
