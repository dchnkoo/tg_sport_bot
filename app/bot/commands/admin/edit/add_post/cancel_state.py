from aiogram.utils.chat_action import ChatActionSender
from .....keyboards.Reply import admin_btns
from aiogram.fsm.context import FSMContext 
from aiogram.filters import and_f, or_f
from .....keyboards.Text import Txt
from .....FSM import models as fsm
from .....routers import admin
from aiogram import types, F


@admin.message(
    and_f(
        or_f(fsm.AddPostState.title,
             fsm.AddPostState.media,
             fsm.AddPostState.text,
             fsm.AddPostState.buttons,
             fsm.AddPostState.confirm),
             F.text == Txt.CANCEL_TXT
    )
)
async def cancel_add_post(msg: types.Message, state: FSMContext):
    async with ChatActionSender.typing(
        bot=msg.bot,
        chat_id=msg.chat.id,
    ):
        await state.clear()

        await msg.answer(
            text="Скасовано.",
            reply_markup=admin_btns,
        )