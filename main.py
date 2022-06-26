from website import app


# Init Slack listeners
import bot.listeners

# Init website routes
import website.routes.homepage
import website.routes.slack_events
import website.routes.get_logs
import website.routes.delete_message_by_user
