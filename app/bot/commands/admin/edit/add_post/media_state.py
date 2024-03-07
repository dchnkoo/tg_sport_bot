from app.settings import MEDIA_LIMIT, PHOTO_LIMMIT, VIDEO_LIMIT
from .....keyboards.Text import txtranslate, TranslateString
from aiogram.utils.chat_action import ChatActionSender
from .....keyboards.Reply import cancel_btns
from aiogram.fsm.context import FSMContext 
from .....FSM import models as fsm
from aiogram.filters import and_f
from .....routers import admin
from aiogram import types, F
import io


@admin.message(
        and_f(fsm.AddPostState.media, F.text == txtranslate.SKIP)
)
async def try_to_skip_media_context(msg: types.Message, state: FSMContext):
    async with ChatActionSender.typing(
        chat_id=msg.chat.id,
        bot=msg.bot,
    ):
        get_data = await state.get_data()
        category = get_data.get("category")

        if category == txtranslate.EXESIZES:
            await msg.answer(
                text=await TranslateString(
                    "Ви не можете пропустити цей крок."
                ).translate_to_lang(msg.from_user.language_code)
            )

            return
        
        await state.update_data(media=[])
        await state.set_state(fsm.AddPostState.text)

        await msg.answer(
            text=await TranslateString(
                "Введіть текст для вашого посту:"
            ).translate_to_lang(msg.from_user.language_code),
            reply_markup=cancel_btns
        )


@admin.message(
        and_f(fsm.AddPostState.media, F.text == txtranslate.GO)
)
async def go_from_media_context(msg: types.Message, state: FSMContext):
    async with ChatActionSender.typing(
        chat_id=msg.chat.id,
        bot=msg.bot
    ):
        get_data = await state.get_data()
        media = get_data.get("media")

        if len(media) < 1:
            await msg.answer(
                text=await TranslateString(
                    "Для того щоб піти далі вам потрібно додати хочаб одне фото/відео."
                ).translate_to_lang(msg.from_user.language_code)
            )

            return
        
        await state.set_state(fsm.AddPostState.text)
        await state.update_data(media=media[:MEDIA_LIMIT])
        await msg.answer(
            text=await TranslateString(
                "Введіть текст для вашого посту:"
            ).translate_to_lang(msg.from_user.language_code),
            reply_markup=cancel_btns
        )



@admin.message(
    and_f(fsm.AddPostState.media, F.photo | F.video, ~F.caption)
)
async def set_media_context(msg: types.Message, state: FSMContext):
    async with ChatActionSender.typing(
        chat_id=msg.chat.id,
        bot=msg.bot,
    ):
        content_type = msg.content_type.removeprefix("Content_type.")
        content = msg.video if content_type == "video" else msg.photo[-1]

        LIMIT: int = VIDEO_LIMIT if content_type == "video" else PHOTO_LIMMIT


        get_size = lambda x: int((x / 1024) / 1024)

        size = get_size(content.file_size)
        if size > LIMIT:
            await msg.answer(
                text=await TranslateString(
                    f"Ваше {content_type} не повинно займати більше {LIMIT}! У вас {size}"
                ).translate_to_lang(msg.from_user.language_code)
            )

            return
        
        file_id: str = content.file_id
        data = await state.get_data()
        media: list = data.get("media")

        if len(media) < MEDIA_LIMIT:
            buffer = io.BytesIO()

            await msg.bot.download(file_id, buffer)

            value: bytes = buffer.getvalue()

            media.append([content_type, value])

            data: dict = await state.update_data(media=media)
        
            await msg.answer(
                text=await TranslateString(
                    f"Додано {content_type} в медіа, ще {len(data.get('media'))}/{MEDIA_LIMIT}"
                ).translate_to_lang(msg.from_user.language_code)
            )
        else:
            await msg.answer(
                await TranslateString(
                    f"Ви не можете додати більше {MEDIA_LIMIT} фотографії до посту. Натисніть кнопку -> {txtranslate.GO}"
                ).translate_to_lang(msg.from_user.language_code)
            )


@admin.message(
    fsm.AddPostState.media
)
async def not_correct_context_for_media(msg: types.Message):
    await msg.answer(
        text=await TranslateString(
            "Відправляйте тільки фото/відео в цьому контексті. Без підпису."
        ).translate_to_lang(msg.from_user.language_code)
    )