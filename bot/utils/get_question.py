import os
import requests


ENDPOINT_URL = 'https://br-helper.com/brainly/task'
TOOLS_AUTH_TOKEN = os.environ['TOOLS_AUTH_TOKEN']


def get_question(id: int) -> dict:
    """Get a Brainly question by ID"""
    url = f"{ENDPOINT_URL}/{id}"
    headers = {
        'authorization': f"basic {TOOLS_AUTH_TOKEN}"
    }

    r = requests.get(url, headers=headers)

    return r.json()
