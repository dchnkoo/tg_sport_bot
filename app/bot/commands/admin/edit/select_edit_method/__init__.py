from app.bot.keyboards.Inline.admin.edit_callback import AdminEditKeyBoardCallbackData
from app.bot.keyboards.CallbackModels.admin import EditCallbackData
from app.bot.keyboards.Text.object import EditBtnTxt

from .....routers.admin import admin
from aiogram import types, F


@admin.callback_query(
    EditCallbackData.filter(F.type.startswith(EditBtnTxt.type))
)
async def edit_callback_data_type(callback: types.CallbackQuery, callback_data: EditCallbackData):
    data = callback_data.type.removeprefix(EditBtnTxt.type)
    type = EditBtnTxt.type

    keyboard = AdminEditKeyBoardCallbackData()

    await callback.message.edit_text(
        text=f"Які зміни хочете зробити для {type} в {data}?",
        reply_markup=keyboard.get_buttons(type + data)
    )



@admin.callback_query(
    EditCallbackData.filter(F.type.startswith(EditBtnTxt.post))
)
async def edit_callback_data_type(callback: types.CallbackQuery, callback_data: EditCallbackData):
    data = callback_data.type.removeprefix(EditBtnTxt.post)
    post = EditBtnTxt.post

    keyboard = AdminEditKeyBoardCallbackData()

    await callback.message.edit_text(
        text=f"Які зміни хочете зробити для {post} в {data}?",
        reply_markup=keyboard.get_buttons(post + data)
    )