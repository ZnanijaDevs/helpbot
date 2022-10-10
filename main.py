# pylint: disable=unused-import
from webapp import app

# Init Sentry
import init_sentry

# Init Slack event listeners
import bot.events

# Init webapp routes
import webapp.routes.homepage
import webapp.routes.slack_events
import webapp.routes.delete_message_by_user
