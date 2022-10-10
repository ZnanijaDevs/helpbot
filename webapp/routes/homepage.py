from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from webapp import app, templates
from bot.database import redis
from getenv import env


@app.get('/', response_class=HTMLResponse)
async def homepage(request: Request):
    messages_in_db = redis.keys('todelete:*')

    context = {
        'request': request,
        'mode': env('MODE'),
        'messages_count': len(messages_in_db)
    }

    return templates.TemplateResponse(name='homepage.html', context=context)
