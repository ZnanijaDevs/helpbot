from fastapi import Request
from bot import events_handler
from website.app import app

# Init Slack events listeners
import bot.listeners

@app.post("/slack_events")
async def handle_slack_events(request: Request):
    return await events_handler.handle(request)
