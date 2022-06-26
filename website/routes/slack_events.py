from fastapi import Request

from bot import events_handler
from website import app


@app.post('/slack_events')
async def handle_slack_events(request: Request):
    return await events_handler.handle(request)
