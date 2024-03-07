from aiogram.filters import CommandStart, Command, and_f, or_f
from app.bot.keyboards.Reply import admin_btns
from ....language import TranslateString
from ....filters import isAdmin
from ...object import Commands
from ....routers import admin
from aiogram import types


@admin.message(
        and_f(or_f(CommandStart(), Command(Commands.HOME)), isAdmin())
)
async def start_message(msg: types.Message):
    text = await TranslateString(
        "Привіт {}! Ви маєте доступ до панелі адміністратора."
    ).translate_to_lang(msg.from_user.language_code)

    await msg.answer(
        text=text.format(msg.from_user.full_name),
        reply_markup=admin_btns
    )