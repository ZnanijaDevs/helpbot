import os
from datetime import datetime
import pytz
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from website.app import app, templates
from bot.database import redis


@app.get('/', response_class=HTMLResponse)
async def homepage(request: Request):
    now = datetime.now(pytz.timezone('Europe/Kiev'))
    mode = os.environ['MODE']
    source_url = 'https://github.com/vlaex/helpbot-spamouts'

    matches = redis.keys('todelete:*')

    context = {
        'request': request,
        'server_time': now.strftime('%m/%d/%Y, %H:%M:%S'),
        'mode': mode,
        'source_url': source_url,
        'messages_count': len(matches)
    }

    return templates.TemplateResponse(
        name='homepage.html',
        context=context,
        headers={
            'x-bot-mode': mode,
            'cache-control': 'max-age=300'
        }
    )