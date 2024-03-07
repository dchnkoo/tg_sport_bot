from .....keyboards.Text import txtranslate, TranslateString
from aiogram.utils.chat_action import ChatActionSender
from .....keyboards.Reply import confirm_btns
from .....msg.builder import BuildTelegramMsg
from aiogram.fsm.context import FSMContext
from .....FSM import models as fsm
from .....filters import isButtons
from aiogram.filters import and_f
from .....regex import check_text
from .....routers import admin
from aiogram import types, F


@admin.message(
    and_f(fsm.AddPostState.buttons, isButtons())
)
async def get_buttons_state(msg: types.Message, state: FSMContext):
    buttons = tuple(tuple(zip(("text", "url"), i)) for i in 
            [(text.strip(), url.strip()) for text, url in check_text(msg.text)])

    async with ChatActionSender.typing(
        bot=msg.bot,
        chat_id=msg.chat.id,
    ):
        await state.set_state(fsm.AddPostState.confirm)
        new_data: dict = await state.update_data(buttons=buttons)

        await build_end_send_post_to_confirm(msg, new_data)
    

@admin.message(
        and_f(fsm.AddPostState.buttons, F.text == txtranslate.SKIP)
)
async def skip_btns_state(msg: types.Message, state: FSMContext):
    async with ChatActionSender.typing(
        bot=msg.bot,
        chat_id=msg.chat.id,
    ):
        await state.set_state(fsm.AddPostState.confirm)
        data: dict = await state.get_data()

        await build_end_send_post_to_confirm(msg, data)


async def build_end_send_post_to_confirm(msg: types.Message, data: dict):
    media = data.get("media")

    message = BuildTelegramMsg(
        title=data.get("title"),
        media=media,
        text=data.get("text"),
        buttons=data.get("buttons"),
        type=data.get("type")
    )

    if media:
        await msg.answer_media_group(
            media=message.get_media_group()
        )
        
    await msg.answer(**message.get_msg())

    await msg.answer(
            text=await TranslateString(
                "Додати пост?"
            ).translate_to_lang(msg.from_user.language_code),
            reply_markup=confirm_btns
        )

@admin.message(
    and_f(fsm.AddPostState.buttons)
)
async def not_correct_context_buttons(msg: types.Message):
    await msg.answer(
        text=await TranslateString(
            "Не знайдено жодної кнопки."
        ).translate_to_lang(msg.from_user.language_code)
    )