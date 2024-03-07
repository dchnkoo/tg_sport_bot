from .....keyboards.Text import txtranslate, TranslateString
from .....keyboards.Reply import confirm_btns, admin_btns
from aiogram.utils.chat_action import ChatActionSender
from .....models import ModelDataManipulation
from aiogram.fsm.context import FSMContext
from .....FSM import models as fsm
from aiogram.filters import and_f
from .....routers import admin
from aiogram import types, F
import base64


@admin.message(
    and_f(fsm.AddPostState.confirm, F.text == txtranslate.CONFIRM)
)
async def add_post_to_db(msg: types.Message, state: FSMContext):
    async with ChatActionSender.typing(
        chat_id=msg.chat.id,
        bot=msg.bot
    ):
        data: dict = await state.get_data()
        category = data.pop("category")
        data.pop("confirm", None)

        media = data.get("media")
        data.update(media=[[content, base64.b64encode(value).decode("utf-8")] for content, value in media])

        model = ModelDataManipulation(category, media=True)
        _, message = await model.insert_data(**data)

        await state.clear()
        await msg.answer(
            text=await TranslateString(message).translate_to_lang(msg.from_user.language_code),
            reply_markup=admin_btns
        )


@admin.message(
    fsm.AddPostState.confirm
)
async def not_correct_confirmation(msg: types.Message):
    await msg.answer(
        text=await TranslateString(
            "Виберіть один з варіантів нижче:"
        ).translate_to_lang(msg.from_user.language_code),
        reply_markup=confirm_btns
    )
