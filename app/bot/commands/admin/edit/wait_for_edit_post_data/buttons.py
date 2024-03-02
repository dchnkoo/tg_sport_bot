from app.bot.keyboards.Reply.cancel import CancelReplyButton
from aiogram.utils.chat_action import ChatActionSender
from app.bot.keyboards.Text.object import CancleBtns
from app.bot.msg.builder import BuildTelegramMsg
from aiogram.fsm.context import FSMContext
from .....routers.admin import admin
from .fsm_models import PostForm
from aiogram import types, F
from regex import regex


@admin.message(PostForm.buttons, F.text == CancleBtns.skip)
async def skip_buttons(msg: types.Message, state: FSMContext):
    async with ChatActionSender.typing(
        chat_id=msg.chat.id,
        bot=msg.bot
    ):
        new_data = await state.update_data(buttons=[])
        await state.set_state(PostForm.confirm)

    message = BuildTelegramMsg(
        title=new_data.get("title"),
        media=new_data.get("media"),
        text=new_data.get("text"),
        buttons=new_data.get("buttons"),
        type=new_data.get("type")
    )

    await msg.answer_media_group(
        media=message.get_media_group()
    )
    await msg.answer(**message.get_msg())


    keyboard = CancelReplyButton()
    await msg.answer(
        text="Додати пост?",
        reply_markup=keyboard.get_buttons(confirm=True)
    )


check_text = lambda x: regex.findall("(.+)-(.+)", x)

@admin.message(PostForm.buttons, F.text, ~F.text.startswith("/"))
async def get_urls_buttons(msg: types.Message, state: FSMContext):
    buttons: list[tuple[str]] = [(txt.strip(), url.strip()) for txt, url in check_text(msg.text)]

    if not buttons:
        await msg.answer(
            text="Не було знайдено жодної кнопки. Не коректний формат."
        )

        return
    
    if len(buttons) > 3:
        await msg.answer(
            text="Не можливо додати більше трьох посилань."
        )

        return  
    
    
    async with ChatActionSender.typing(
        chat_id=msg.chat.id,
        bot=msg.bot
    ):
        new_data: dict = await state.update_data(buttons=tuple(tuple(zip(("text", "url"), i)) for i in buttons))
        await state.set_state(PostForm.confirm)

        
        message = BuildTelegramMsg(
            title=new_data.get("title"),
            media=new_data.get("media"),
            text=new_data.get("text"),
            buttons=new_data.get("buttons"),
            type=new_data.get("type")
        )

        await msg.answer_media_group(
            media=message.get_media_group()
        )
        await msg.answer(**message.get_msg())

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