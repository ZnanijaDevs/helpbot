import re
from datetime import datetime
import pytz
from bot.config import DELETE_REASON_REGEX, TASK_ID_REGEX


tz = pytz.timezone('Europe/Moscow')


def ts_to_date(timestamp: str | float) -> str:
    if isinstance(timestamp, str):
        timestamp = float(timestamp)

    return datetime.fromtimestamp(timestamp, tz).strftime('%d.%m.%Y %H:%M:%S')


def get_delete_reason(text: str) -> str:
    match = re.search(DELETE_REASON_REGEX, text, re.IGNORECASE)

    if match is None:
        return ''

    return re.sub(r"(^,|-)\s*|\.$", '', match.group()).strip().capitalize()


def find_task_id(text: str) -> int | None:
    task_id = re.search(TASK_ID_REGEX, text)

    if task_id is None:
        return

    return int(task_id.group())
