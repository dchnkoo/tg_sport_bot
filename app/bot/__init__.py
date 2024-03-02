from .commands.object import CommandsBot
from app.bot.commands import user, admin
from aiogram.methods import DeleteWebhook
from .setup import dp, bot
import logging, asyncio

admin.include_router(
    user,
)

dp.include_routers(
    admin,
)

async def start():
    logging.basicConfig(level=logging.INFO)
    await bot.set_my_commands(CommandsBot.get_bot_commands())

    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

asyncio.run(start())