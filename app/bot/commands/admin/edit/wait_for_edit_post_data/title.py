from app.bot.commands.admin.edit.wait_for_edit_post_data.fsm_models import PostForm
from app.bot.keyboards.Reply.cancel import CancelReplyButton
from app.bot.keyboards.Reply.start import StartButtons
from aiogram.fsm.context import FSMContext
from .....routers.admin import admin
from app.settings import MEDIA_LIMIT
from aiogram import types, F



@admin.message(PostForm.title, F.text)
async def get_title_context(msg: types.Message, state: FSMContext):

    data = await state.update_data(title=msg.text)
    await state.set_state(PostForm.media)

    keyboard = CancelReplyButton()

    can_skip = {"skip": False} if data.get("category").startswith(StartButtons.exesizes) else {"skip": True}

    await msg.answer(
        text=f"Відправте до {MEDIA_LIMIT} Фото/Відео:",
        reply_markup=keyboard.get_buttons(go=True, **can_skip)
    )

@admin.message(PostForm.title)
async def get_title_context(msg: types.Message):
    await msg.answer(
        text="Введіть коректний заголовок."
    )