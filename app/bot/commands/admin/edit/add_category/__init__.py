from .....keyboards.Text import txtranslate, TranslateString
from .....keyboards.Reply import cancel_btns, admin_btns
from aiogram.utils.chat_action import ChatActionSender
from .....models import ModelDataManipulation
from aiogram.fsm.context import FSMContext
from ....callbacks import models as clbck
from .....FSM import models as fsm
from aiogram.filters import and_f
from .....routers import admin
from aiogram import types, F


@admin.callback_query(
    clbck.AddCategory.filter()
)
async def start_add_category_context(callback: types.CallbackQuery, callback_data: clbck.AddCategory, state: FSMContext):
    model, language = callback_data.type, callback_data.lang

    async with ChatActionSender.typing(
        chat_id=callback.message.chat.id,
        bot=callback.bot,
    ):
        await state.set_state(fsm.AddCategoryState.category)
        await state.update_data(type=model)

        await callback.message.delete()
        await callback.bot.send_message(
            chat_id=callback.message.chat.id,
            text=await TranslateString(
                f"Введіть назву категорії яку бажаєте додати для {model}:"
            ).translate_to_lang(language),
            reply_markup=cancel_btns
        )


@admin.message(
    and_f(fsm.AddCategoryState.category, 
          F.text, ~F.text.startswith("/"),
          F.text != txtranslate.CANCEL_TXT)
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
            text=await TranslateString(message).translate_to_lang(msg.from_user.language_code),
        )


@admin.message(
        and_f(fsm.AddCategoryState.category, F.text == txtranslate.CANCEL_TXT)
)
async def cancel_add_category(msg: types.Message, state: FSMContext):
    async with ChatActionSender.typing(
        chat_id=msg.chat.id,
        bot=msg.bot
    ):
        await state.clear()

        await msg.answer(
            text=await TranslateString(
                "Скасовано"
            ).translate_to_lang(msg.from_user.language_code),
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
            await TranslateString(
                "Введіть коректну назву категорії."
            ).translate_to_lang(msg.from_user.language_code),
        )