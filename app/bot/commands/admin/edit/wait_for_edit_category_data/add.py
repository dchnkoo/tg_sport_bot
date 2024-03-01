from app.bot.keyboards.CallbackModels.admin import AddCallbackData
from app.bot.keyboards.Text.object import EditBtnTxt, CancleBtns
from app.bot.keyboards.Reply.cancel import CancelReplyButton
from app.bot.keyboards.Reply.start import StartButtons
from .insert_category import get_correct_table, insert_into_table

from aiogram.utils.chat_action import ChatActionSender
from aiogram.fsm.context import FSMContext
from .fsm_model import AddFormCategory
from .....routers.admin import admin
from aiogram.filters import and_f
from aiogram import types, F


@admin.callback_query(
    AddCallbackData.filter(F.type.startswith(EditBtnTxt.type))
)
async def wait_for_type_data(callback: types.CallbackQuery, callback_data: AddCallbackData, state: FSMContext):
    data = callback_data.type.removeprefix(EditBtnTxt.type)
  
    await state.update_data(type=data)
    await state.set_state(AddFormCategory.category)

    keyboard = CancelReplyButton()

    await callback.message.delete()
    await callback.bot.send_message(
        chat_id=callback.message.chat.id,
        text=f"Що бажаєте додати в {EditBtnTxt.type} {data}?\nВведіть нижче:",
        reply_markup=keyboard.get_buttons()
    )



@admin.message(and_f(AddFormCategory.category, F.text != CancleBtns.cancel, F.text.not_contains("/")))
async def procces_add_category(msg: types.Message, state: FSMContext):
    await state.update_data(category=msg.text)
    data = await state.get_data()

    async with ChatActionSender.typing(
        bot=msg.bot,
        chat_id=msg.chat.id,
    ):
        new_data = await get_correct_table(insert_into_table, **data)
        keyboard = StartButtons()

        await state.clear()
    await msg.answer(text=new_data, reply_markup=keyboard.get_buttons())



@admin.message(and_f(AddFormCategory.category, F.text.startswith("/")))
async def procces_nocorrect_add_category(msg: types.Message):
    await msg.answer("Введіть коректну назву для категорії")



@admin.message(F.text == CancleBtns.cancel)
async def cancel_fsm_handler(msg: types.Message, state: FSMContext):

    current_state = await state.get_state()
    if current_state is None:
        return
    
    await state.clear()
    keyboard = StartButtons()

    await msg.answer(
        "Скасовано.",
        reply_markup=keyboard.get_buttons()
    )