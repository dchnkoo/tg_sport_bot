from app.bot.keyboards.Reply.cancel import CancelReplyButton
from aiogram.utils.chat_action import ChatActionSender
from app.bot.keyboards.Text.object import CancleBtns
from aiogram.fsm.context import FSMContext
from .....routers.admin import admin
from .fsm_models import PostForm
from aiogram import types, F
from regex import regex


check_text = lambda x: regex.findall("([\\w\\s]+) ?- ?(.+)", x)

@admin.message(PostForm.buttons, F.text, ~F.text.startswith("/"))
async def get_urls_buttons(msg: types.Message, state: FSMContext):
    buttons = check_text(msg.text)

    if not buttons:
        await msg.answer(
            text="Не було знайдено жодної кнопки. Не коректний формат."
        )

        return
    
    async with ChatActionSender.typing(
        chat_id=msg.chat.id,
        bot=msg.bot
    ):
        await state.update_data(buttons=tuple(tuple(zip(("text", "url"), i)) for i in buttons))
        await state.set_state(PostForm.confirm)

        keyboard = CancelReplyButton()
        await msg.answer(
            text="Додати пост?",
            reply_markup=keyboard.get_buttons(confirm=True)
        )


@admin.message(PostForm.buttons, F.text == CancleBtns.skip)
async def skip_buttons(msg: types.Message, state: FSMContext):
    async with ChatActionSender.typing(
        chat_id=msg.chat.id,
        bot=msg.bot
    ):
        await state.update_data(buttons=[])
        await state.set_state(PostForm.confirm)

    keyboard = CancelReplyButton()
    await msg.answer(
        text="Додати пост?",
        reply_markup=keyboard.get_buttons(confirm=True)
    )


@admin.message(PostForm.buttons)
async def not_correct_buttons(msg: types.Message):
    await msg.answer(
        text="Не коректний формат."
    )