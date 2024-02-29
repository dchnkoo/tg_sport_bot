from aiogram.filters import CommandStart, Command, and_f, or_f
from ....keyboards.Reply.start import StartButtons
from ....routers.user import user
from ....filters.user import isUser
from aiogram import types
from ...object import CommandsBot



@user.message(and_f(or_f(CommandStart(), Command(CommandsBot.HOME.no_prefix)), isUser()))
async def user_start(msg: types.Message):

    await msg.answer(
        text="Hello World!"
    )