from bot import bot


async def get_user(id: str):
    """Retrieve information about a Slack user"""

    data = await bot.client.users_info(user=id)
    user = data['user']

    return user | {
        'nick': user['profile']['display_name'] or user['name']
    }
