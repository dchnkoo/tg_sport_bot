from app.bot.keyboards.CallbackModels.admin import EditCallbackBtn
from app.bot.keyboards.Text.object import CancleBtns
from .....routers.admin import admin

from aiogram.fsm.context import FSMContext
from aiogram import types, F


@admin.callback_query(
    EditCallbackBtn.filter(F.type == CancleBtns.cancel)
)
async def cancel_edit_callback_data(callback: types.CallbackQuery):
    await callback.message.delete()