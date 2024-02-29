from aiogram.client.session.aiohttp import AiohttpSession
from aiogram import Bot, Dispatcher
from app.settings import BOT_TOKEN
import os


env = os.environ

session = AiohttpSession()
bot = Bot(env.get("BOT_TOKEN", BOT_TOKEN), session=session)
dp = Dispatcher()