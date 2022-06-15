import re
import json
from bot import bot
from bot.config import PROFILE_LINK_REGEX
from bot.utils import get_delete_reason
from bot.utils.brainly_graphql import client, to_base64
from bot.database import redis


@bot.message(re.compile(PROFILE_LINK_REGEX))
async def save_message(message, context, logger):
    profile_link = re.search(PROFILE_LINK_REGEX, message['text'])

    if profile_link is None:
        logger.info(f"Failed to find the profile link in the message: {message['text']}")
        return

    profile_link = profile_link.group()
    user = context.get('user_data')

    user_id = profile_link.split('-')[-1]
    encoded_user_id = to_base64(user_id, 'user')

    # Fetch user data
    user_data = await client.execute_async(query="""
        query GetUser($id: ID!) {
            user(id: $id) {
                nick
                rank {name}
                points
                answers {count}
                avatar {url}
                thanks {count}
                created
                helpedUsersCount
            }
        }
    """, variables={'id': encoded_user_id})

    if not user_data['data'] or not user_data['data']['user']:
        logger.info(f"No user data ({profile_link}): {user_data}")
        return

    brainly_user = user_data['data']['user']

    data = {
        'sent_by': context.get('user_nick'),
        'reason': get_delete_reason(message['text']),
        'link': profile_link,
        'user': {
            'id': encoded_user_id,
            'database_id': int(user_id),
            'nick': brainly_user['nick'],
            'rank': brainly_user['rank']['name'] if brainly_user['rank'] else '',
            'points': brainly_user['points'],
            'answers_count': brainly_user['answers']['count'],
            'avatar': brainly_user['avatar']['url'] if brainly_user['avatar'] else '/img/avatars/100-ON.png',
            'thanks_count': brainly_user['thanks']['count'],
            'created': brainly_user['created'],
            'helped_users_count': brainly_user['helpedUsersCount']
        },
        'message': {
            'text': message['text'],
            'ts': message['ts']
        },
        'sender': {
            'id': user['id'],
            'team_id': user['team_id'],
            'nick': context.get('user_nick'),
            'avatar': user['profile']['image_192']
        }
    }

    # Save message data in the Redis storage
    redis.set(
        f"todelete:{user_id}:{message['ts']}:{message['user']}",
        json.dumps(data)
    )
