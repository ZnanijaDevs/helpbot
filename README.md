# helpbot

This bot is designed for the Slack workspace for our moderation team.

This repository is licensed under _the MIT license_.

### Run the bot
Create `.env.debug` or `.env.prod`
```
# Mode
MODE=development

# Bot tokens
SLACK_USER_TOKEN=xoxp-111111111-1111111111-1111111111-1111111111111111111111111
SLACK_ADMIN_TOKEN=xoxp-111111111-1111111111-1111111111-1111111111111111111111111
SLACK_BOT_TOKEN=xoxb-11111111111-111111111111-111111111111111
SLACK_SIGNING_SECRET=1234567890abcdef

# Slack config
CHANNEL_ANTISPAMERS_ID=C03G81FJEFN
CHANNEL_HELP_ID=C03FS2C9F0W
CHANNEL_TO_DELETE_ID=C03FYSX0N3U
CHANNEL_MODERATORS_ID=C03KCFD812B

# Redis config
REDIS_DB_URL = "redis://admin:12345@localhost:15574"

# Google Sheets config [use Google service account to access Sheets API]
SERVICE_ACCOUNT_PRIVATE_KEY_ID=123456789abcwfhiweihr
SERVICE_ACCOUNT_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\n12345678123456789\n-----END PRIVATE KEY-----\n
SERVICE_ACCOUNT_CERT_URL=https://www.googleapis.com/robot/v1/metadata/gserviceaccount.com
SERVICE_ACCOUNT_CLIENT_ID=123456789

TOOLS_AUTH_TOKEN=base64_auth_token
SENTRY_DSN=https://xxx@xxx.ingest.sentry.io/111
```
Install the requirements and run the server.
```bash
$ pip install -r requirements.txt
$ uvicorn app.main:app --reload
```