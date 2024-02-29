from app.bot.keyboards.Inline.admin.edit_callback import AdminKeyboardDelete, DeleteCallbackData
from app.bot.keyboards.CallbackModels.admin import DeleteCallbackData
from app.bot.keyboards.Text.object import EditBtnTxt, StartButtonsTxt
from app.bot.keyboards.Reply.confirm import ConfirmButtons
from .get_data_with_pagination import get_category_with_pages
from .delete_category_data import delete_from_db_by_id
from app.bot.keyboards.Reply.start import StartButtons
from .insert_category import get_correct_table
from .....routers.admin import admin
from .fsm_model import ConfirmDelete

from aiogram.fsm.context import FSMContext
from aiogram.filters import and_f
from aiogram import types, F


@admin.callback_query(DeleteCallbackData.filter(F.type.startswith(EditBtnTxt.type)))
async def select_to_delete(callback: types.CallbackQuery, callback_data: DeleteCallbackData):
    data = callback_data.type.removeprefix(EditBtnTxt.type)

    type = StartButtonsTxt.get_attr(data)
    page = int(data.removeprefix(type))
    
    get = await get_correct_table(get_category_with_pages, **{"type": type, "page": page})

    keyboard = AdminKeyboardDelete()

    await callback.message.edit_text(
        text=f"Для видалення категорії з {type} просто натисніть на неї:", 
        reply_markup=keyboard.get_buttons(get[0], get[1], page, EditBtnTxt.type + type)
    )


@admin.callback_query(DeleteCallbackData.filter(F.type.startswith(EditBtnTxt.delete)))
async def delete_category(callback: types.CallbackQuery, callback_data: DeleteCallbackData, state: FSMContext):
    data = callback_data.type.removeprefix(EditBtnTxt.delete)

    type: str = StartButtonsTxt.get_attr(data)
    identity = int(data.removeprefix(type))

    await state.set_state(ConfirmDelete.confirm)
    await state.update_data(type=type, identity=identity)

    keyboard = ConfirmButtons()
    await callback.message.delete()
    await callback.bot.send_message(
        chat_id=callback.message.chat.id,
        text="Підтверідть видалення:",
        reply_markup=keyboard.get_buttons()
    )


@admin.message(and_f(ConfirmDelete.confirm, F.text == EditBtnTxt.confirm))
async def confirm_delete_category(msg: types.Message, state: FSMContext):

    data = await state.get_data()
    await state.clear()

    delete = await get_correct_table(delete_from_db_by_id, **data)
    keyboard = StartButtons()

    await msg.answer(
        text=delete,
        reply_markup=keyboard.get_buttons()
    )


@admin.message(and_f(ConfirmDelete.confirm, F.text == EditBtnTxt.cancel))
async def cancel_delete_category(msg: types.Message, state: FSMContext):

    await state.clear()

    keyboard = StartButtons()
    await msg.answer(
        text=EditBtnTxt.cancel,
        reply_markup=keyboard.get_buttons()
    )

@admin.message(and_f(ConfirmDelete.confirm, F.text != (EditBtnTxt.cancel or EditBtnTxt.confirm)))
async def proccesed_invalid_msg(msg: types.Message):
    keyboard = ConfirmButtons()

    await msg.answer(
        "Виберіть одну з відповідей наведених нижче:",
        reply_markup=keyboard.get_buttons()
        )

