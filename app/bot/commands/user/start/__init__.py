from ....language.bot_answers import USER_START_MSG
from aiogram.filters import CommandStart, Command, or_f
from ...object import Commands
from ....routers import user
from aiogram import types


@user.message(
    or_f(CommandStart(), Command(Commands.HOME))
)
async def user_start(msg: types.Message):
    language = msg.from_user.language_code

    text: str = await USER_START_MSG.translate_to_lang(language)

    await msg.answer(
        text=text.format(msg.from_user.full_name)
    )