from app.bot.keyboards.Reply.cancel import CancelReplyButton, CancleBtns
from app.bot.keyboards.Reply.start import StartButtons
from app.bot.keyboards.Text.object import EditBtnTxt

from app.settings import MEDIA_LIMIT, VIDEO_LIMIT, PHOTO_LIMMIT
from aiogram.utils.chat_action import ChatActionSender
from .file_size import get_human_readable_size_mb
from aiogram.fsm.context import FSMContext
from .....routers.admin import admin
from .fsm_models import PostForm
from aiogram import types, F
import io


@admin.message(PostForm.media, F.text == EditBtnTxt.skip)
async def skip_media_context(msg: types.Message, state: FSMContext):
    data = await state.update_data(media=[])

    if data.get("category").startswith(StartButtons.exesizes):
        await msg.answer(
            text="Ви не можете пропустити цей крок в цій категорії"
        )

    else:
        await state.set_state(PostForm.text)
        
        keyboard = CancelReplyButton()
        await msg.answer(
            f"Введіть текст для вашого посту:", 
            reply_markup=keyboard.get_buttons())


@admin.message(PostForm.media, F.text == EditBtnTxt.go)
async def go_media_context(msg: types.Message, state: FSMContext):
    data = await state.get_data()

    if len(data.get("media")) < 1:
        await msg.answer(
            text="Ви повинні додати хоча б одне фото/відео",
        )
    else:
        media: list = data.get("media")
        data: dict = await state.update_data(media=media[:MEDIA_LIMIT])
        await state.set_state(PostForm.text)

        keyboard = CancelReplyButton()
        await msg.answer(
            f"Введіть текст для вашого посту:", 
            reply_markup=keyboard.get_buttons())


@admin.message(PostForm.media, F.video | F.photo, ~F.caption)
async def get_video_or_photo_context(msg: types.Message, state: FSMContext):
    content_type: str = msg.content_type.removeprefix("ContentType.").upper()
    content = msg.video if content_type == "VIDEO" else msg.photo[-1]

    LIMIT: int = VIDEO_LIMIT if content_type == "VIDEO" else PHOTO_LIMMIT 

    file_id: str = content.file_id
    data: dict = await state.get_data()

    get_size: int = get_human_readable_size_mb(content.file_size)
    if get_size > LIMIT:
        await msg.answer(
            text=f"Відео не повинно бути більше ніж {LIMIT} MB\nВаше відео займає {get_size} MB"
        )

        return

    if len(data.get('media')) < MEDIA_LIMIT:
        buffer = io.BytesIO()
        async with ChatActionSender.typing(
            chat_id=msg.chat.id,
            bot=msg.bot
        ):
            await msg.bot.download(file_id, buffer)
            
            value: bytes = buffer.getvalue()

            media: list = data.get("media")

            media.append([content_type, value])

            data: dict = await state.update_data(media=media)

        await msg.answer(
            text=f"Додано {'відео' if content_type == 'VIDEO' else 'фото'} в медіа, ще {len(data.get('media'))}/{MEDIA_LIMIT}"
        )
    
    else:
        await msg.answer(f"Ви не можете додати більше {MEDIA_LIMIT} фотографії до посту. Натисніть кнопку -> {CancleBtns.go}")

        

@admin.message(PostForm.media, F.photo | F.video, F.caption)
async def not_correct_media_context(msg: types.Message):
    await msg.answer(
        text="Надсилайте медіа без тексту під ним."
    )

@admin.message(PostForm.media)
async def not_correct_media(msg: types.Message):
    await msg.answer(
        text="Надсилайте тільки фото/відео в цьому контексті"
    )