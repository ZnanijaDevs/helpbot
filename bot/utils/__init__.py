import re
from typing import Union
from datetime import datetime
import pytz
from bot.config import DELETE_REASON_REGEX, TASK_ID_REGEX


tz = pytz.timezone('Europe/Moscow')

def ts_to_date(timestamp: str) -> str:
    return datetime.fromtimestamp(float(timestamp), tz).strftime('%d.%m.%Y %H:%M:%S')


def get_delete_reason(text: str) -> str:
    match = re.search(DELETE_REASON_REGEX, text, re.IGNORECASE)

    if match is None:
        return ''

    return re.sub(r"(^,|-)\s*|\.$", '', match.group()).strip().capitalize()


def find_task_id(text: str) -> Union[None, int]:
    task_id = re.search(TASK_ID_REGEX, text)

    if task_id is None:
        return

    return int(task_id.group())