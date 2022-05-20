import re
from datetime import datetime
import pytz
from bot.config import DELETE_REASON_REGEX


tz = pytz.timezone('Europe/Moscow')

def ts_to_date(timestamp: str) -> str:
    return datetime.fromtimestamp(float(timestamp), tz).strftime('%d.%m.%Y %H:%M:%S')


def get_delete_reason(text: str):
    match = re.search(DELETE_REASON_REGEX, text, re.IGNORECASE)

    if match is None:
        return ''

    return re.sub(r"(^,|-)\s*|\.$", '', match.group()).strip().capitalize()
