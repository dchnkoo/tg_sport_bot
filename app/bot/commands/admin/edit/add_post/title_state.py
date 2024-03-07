from .....keyboards.Text import txtranslate, TranslateString
from aiogram.utils.chat_action import ChatActionSender
from .....keyboards.Reply import get_media_btns
from aiogram.fsm.context import FSMContext 
from app.settings import MEDIA_LIMIT
from .....FSM import models as fsm
from aiogram.filters import and_f
from .....routers import admin
from aiogram import types, F


@admin.message(
    and_f(fsm.AddPostState.title, F.text, ~F.text.startswith("/"))
)
async def set_titile_post(msg: types.Message, state: FSMContext):
    async with ChatActionSender.typing(
        chat_id=msg.chat.id,
        bot=msg.bot
    ):
        data = await state.update_data(title=msg.text)
        await state.set_state(fsm.AddPostState.media)

        await msg.answer(
            text=await TranslateString(
                f"Додайте до {MEDIA_LIMIT} фото/відео:"
            ).translate_to_lang(msg.from_user.language_code),
            reply_markup=get_media_btns(
                skip=True if data.get("category") != txtranslate.EXESIZES else False,
                go=True
            )
        )

@admin.message(
    fsm.AddPostState.title
)
async def not_correct_title(msg: types.Message):
    await msg.answer(
        text=await TranslateString(
            "Введіть коректний заголовок."
        ).translate_to_lang(msg.from_user.language_code),
    )