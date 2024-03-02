from aiogram.filters import CommandStart, Command, and_f, or_f
from ....filters.user import isUser
from ...object import CommandsBot
from ....routers.user import user
from aiogram import types



@user.message(and_f(or_f(CommandStart(), Command(CommandsBot.HOME.no_prefix)), isUser()))
async def user_start(msg: types.Message):

    await msg.answer(
        text="Hello World!"
    )