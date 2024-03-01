from aiogram.filters import Command, and_f, or_f
from aiogram import types, F

from app.bot.keyboards.Text.object import AdminEditBtnTxt
from app.bot.keyboards.Inline.admin.edit import AdminEditKeyBoard
from .....filters.admin import isAdmin
from .....routers.admin import admin
from ....object import CommandsBot


@admin.message(or_f(
        and_f(Command(CommandsBot.EDIT.no_prefix), isAdmin()),
        and_f(F.text == AdminEditBtnTxt.adminbtn, isAdmin())
))
async def edit_data(msg: types.Message):
    keyboard = AdminEditKeyBoard()

    await msg.answer(
        text="Що бажаєте відредагувати?",
        reply_markup=keyboard.get_buttons()
    )