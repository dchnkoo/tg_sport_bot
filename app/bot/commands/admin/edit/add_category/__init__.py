from .....keyboards.Reply import cancel_btns, admin_btns
from aiogram.utils.chat_action import ChatActionSender
from .....models import ModelDataManipulation
from aiogram.fsm.context import FSMContext
from ....callbacks import models as clbck
from .....keyboards.Text import Txt
from .....FSM import models as fsm
from aiogram.filters import and_f
from .....routers import admin
from aiogram import types, F


@admin.callback_query(
    clbck.AddCategory.filter()
)
async def start_add_category_context(callback: types.CallbackQuery, callback_data: clbck.AddCategory, state: FSMContext):
    model = callback_data.type

    async with ChatActionSender.typing(
        chat_id=callback.message.chat.id,
        bot=callback.bot,
    ):
        await state.set_state(fsm.AddCategoryState.category)
        await state.update_data(type=model)

        await callback.message.delete()
        await callback.bot.send_message(
            chat_id=callback.message.chat.id,
            text=f"Введіть назву категорії яку бажаєте додати для {model}:",
            reply_markup=cancel_btns
        )


@admin.message(
    and_f(fsm.AddCategoryState.category, 
          F.text, ~F.text.startswith("/"),
          F.text != Txt.CANCEL_TXT)
)
async def add_category(msg: types.Message, state: FSMContext):
    async with ChatActionSender.typing(
        chat_id=msg.chat.id,
        bot=msg.bot
    ):
        data: dict = await state.get_data()

        model = data.get("type")

        insert_data = ModelDataManipulation(model)

        _, message = await insert_data.insert_data(type=msg.text)

        await state.clear()

        await msg.answer(
            reply_markup=admin_btns,
            text=message,
        )


@admin.message(
        and_f(fsm.AddCategoryState.category, F.text == Txt.CANCEL_TXT)
)
async def cancel_add_category(msg: types.Message, state: FSMContext):
    async with ChatActionSender.typing(
        chat_id=msg.chat.id,
        bot=msg.bot
    ):
        await state.clear()

        await msg.answer(
            text="Скасовано",
            reply_markup=admin_btns
        )


@admin.message(
    fsm.AddCategoryState.category
)
async def not_correct_category_context(msg: types.Message):
    async with ChatActionSender.typing(
        chat_id=msg.chat.id,
        bot=msg.bot
    ):
        await msg.answer(
            "Введіть коректну назву категорії.",
        )