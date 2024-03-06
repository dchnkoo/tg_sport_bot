from aiogram.client.session.aiohttp import AiohttpSession
from app.bot.commands.object import CommandsBot
from aiogram.methods import DeleteWebhook
from app.bot.commands.admin import admin
from app.bot.commands.user import user
from aiogram import Bot, Dispatcher
from app.settings import BOT_TOKEN
import logging, os, asyncio


env = os.environ

session = AiohttpSession()
bot = Bot(env.get("BOT_TOKEN", BOT_TOKEN), session=session)
dp = Dispatcher()

dp.include_routers(
    admin,
    user,
)

async def start():
    logging.basicConfig(level=logging.INFO)
    await bot.set_my_commands(list(CommandsBot()))

    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

asyncio.run(start())