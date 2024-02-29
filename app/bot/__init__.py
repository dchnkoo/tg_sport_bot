import logging, asyncio
from app.bot.commands import user, admin
from .setup import dp, bot
from .commands.object import CommandsBot

admin.include_router(
    user,
)

dp.include_routers(
    admin,
)

async def start():
    logging.basicConfig(level=logging.INFO)
    await bot.set_my_commands(CommandsBot.get_bot_commands())

    await dp.start_polling(bot)

asyncio.run(start())