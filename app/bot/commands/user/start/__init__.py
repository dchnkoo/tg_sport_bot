from aiogram.filters import CommandStart, Command, or_f
from ...object import Commands
from ....routers import user
from aiogram import types


@user.message(
    or_f(CommandStart(), Command(Commands.HOME))
)
async def user_start(msg: types.Message):
    await msg.answer(
        text=f"Привіт {msg.from_user.full_name}! Ласкаво просимо до нашого боту, який допоможе тобі з тренуваннями на різні частини тіла, рекомендаціями щодо харчування та видами тренувань. Готуйся до натхненної подорожі до здоров'я та фітнесу! Якщо ти готовий, давай почнемо! 🏋️‍♂️🥦"
    )