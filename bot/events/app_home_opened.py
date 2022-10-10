from slackblocks import HomeView, SectionBlock, HeaderBlock
from bot import bot


@bot.event('app_home_opened')
async def show_admin_panel(event):
    await bot.client.views_publish(**HomeView(
        user_id=event['user'],
        blocks=[
            HeaderBlock('Администрирование бота'),
            SectionBlock('hi')
        ]
    ))
