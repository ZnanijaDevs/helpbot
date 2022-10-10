import requests
from getenv import env


ENDPOINT_URL = 'https://tools.br-helper.com/brainly/task'
TOOLS_AUTH_TOKEN = env('TOOLS_AUTH_TOKEN')


def get_question(id: int) -> dict:
    """Get a Brainly question by ID"""
    url = f"{ENDPOINT_URL}/{id}"
    headers = {
        'authorization': f"basic {TOOLS_AUTH_TOKEN}"
    }

    r = requests.get(url, headers=headers)

    return r.json()
