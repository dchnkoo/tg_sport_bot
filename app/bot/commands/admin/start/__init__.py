from aiogram.filters import CommandStart, Command, and_f, or_f 
from ....routers.admin import admin
from ....filters.admin import isAdmin
from ....keyboards.Reply.start import StartButtons
from aiogram import types
from ...object import CommandsBot


@admin.message(and_f(or_f(CommandStart(), Command(CommandsBot.HOME.no_prefix)), isAdmin()))
async def admin_start(msg: types.Message):
    keyboard = StartButtons()
    text=(f"Вітаю {msg.from_user.full_name}!\nВи маєте доступ до панелі адміністратора 🕵️")

    await msg.answer(
        text=text,
        reply_markup=keyboard.get_buttons()
    )