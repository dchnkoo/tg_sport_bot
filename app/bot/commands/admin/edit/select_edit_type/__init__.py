from app.bot.keyboards.Inline.admin.edit_callback import AdminEditKeyBoardCallback
from app.bot.keyboards.CallbackModels.admin import EditCallbackBtn
from app.bot.keyboards.Text.object import CancleBtns

from .....routers.admin import admin
from aiogram import types, F


@admin.callback_query(
    EditCallbackBtn.filter(F.type != CancleBtns.cancel)
)
async def edit_callback_data(callback: types.CallbackQuery, callback_data: EditCallbackBtn):
    keyboard = AdminEditKeyBoardCallback()

    
    await callback.message.edit_text(
        text=f"Що бажаєте відредагувати в {callback_data.type}?",
        reply_markup=keyboard.get_buttons(callback_data.type)
    )