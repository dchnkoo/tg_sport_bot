from aiogram.filters import CommandStart, Command, and_f, or_f
from ....filters.user import isUser
from ...object import CommandsBot
from ....routers.user import user
from aiogram import types



@user.message(and_f(or_f(CommandStart(), Command(CommandsBot.HOME.no_prefix)), isUser()))
async def user_start(msg: types.Message):

    await msg.answer(
        text=f"Привіт {msg.from_user.full_name}! Ласкаво просимо до нашого боту, який допоможе тобі з тренуваннями на різні частини тіла, рекомендаціями щодо харчування та видами тренувань. Готуйся до натхненної подорожі до здоров'я та фітнесу! Якщо ти готовий, давай почнемо! 🏋️‍♂️🥦"
    )