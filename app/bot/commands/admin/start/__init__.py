from aiogram.filters import CommandStart, Command, and_f, or_f
from app.bot.keyboards.Reply import admin_btns
from ....filters import isAdmin
from ...object import Commands
from ....routers import admin
from aiogram import types


@admin.message(
        and_f(or_f(CommandStart(), Command(Commands.HOME)), isAdmin())
)
async def start_message(msg: types.Message):
    await msg.answer(
        text=f"Вітаю {msg.from_user.full_name}! Ви маєте доступ до панелі адміністратора.",
        reply_markup=admin_btns
    )