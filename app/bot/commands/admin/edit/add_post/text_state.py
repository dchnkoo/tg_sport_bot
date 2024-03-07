from aiogram.utils.chat_action import ChatActionSender
from .....keyboards.Reply import get_media_btns
from aiogram.fsm.context import FSMContext 
from .....language import TranslateString
from .....FSM import models as fsm
from .....routers import admin
from aiogram import types, F


@admin.message(fsm.AddPostState.text, F.text, ~F.text.startswith("/"))
async def get_text_context(msg: types.Message, state: FSMContext):
    async with ChatActionSender.typing(
        bot=msg.bot,
        chat_id=msg.chat.id
    ):

        if len(msg.text) > 4000:
            await msg.answer(
                text=await TranslateString(
                    f"Пост не може перевищувати 4000 символів, у вас {len(msg.text)} символів"
                ).translate_to_lang(msg.from_user.language_code)
            )

            return
    
        await state.update_data(text=msg.text)                     

        await state.set_state(fsm.AddPostState.buttons)

        btns_add = "Додайте кнопки які будуть містити посилання на будь-який ресурс\nВ форматі:\n\n\t\tТекст кнопки - url\n\t\tТекст кнопки 2 - url"

        warn = "\n\nМаксимально можливо додати 3 кнопки"

    await msg.answer(   
        text=await TranslateString(
            btns_add + warn
        ).translate_to_lang(msg.from_user.language_code),
        reply_markup=get_media_btns(skip=True)
    )
    

@admin.message(fsm.AddPostState.text)
async def not_correct_text(msg: types.Message):
    await msg.answer(
        text=await TranslateString(
            "Напиішть текстове повідомлення для вашого посту."
        ).translate_to_lang(msg.from_user.language_code)
    )