from app.bot.keyboards.Reply.cancel import CancelReplyButton
from aiogram.utils.chat_action import ChatActionSender
from aiogram.fsm.context import FSMContext
from .....routers.admin import admin
from .fsm_models import PostForm
from aiogram import types, F


# TEXT
@admin.message(PostForm.text, F.text, ~F.text.startswith("/"))
async def get_text_context(msg: types.Message, state: FSMContext):
    await state.update_data(text=msg.text)

    if len(msg.text) > 4000:
        await msg.answer(
            text=f"Пост не може перевищувати 4000 символів, у вас {len(msg.text)} символів"
        )

        return

    async with ChatActionSender.typing(
        bot=msg.bot,
        chat_id=msg.chat.id
    ):
        await state.set_state(PostForm.buttons)

        keyboard = CancelReplyButton()

        btns_add = "Додайте кнопки які будуть містити посилання на будь-який ресурс\nВ форматі:\n\n\t\tТекст кнопки - url\n\t\tТекст кнопки 2 - url"

        warn = "\n\nМаксимально можливо додати 3 кнопки"

    await msg.answer(   
        text=btns_add + warn,
        reply_markup=keyboard.get_buttons(skip=True)
    )
    

@admin.message(PostForm.text)
async def not_correct_text(msg: types.Message):
    await msg.answer(
        text="Напиішть текстове повідомлення для вашого посту."
    )