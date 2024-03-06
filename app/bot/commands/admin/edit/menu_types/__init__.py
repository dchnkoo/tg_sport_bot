from app.bot.keyboards.Inline.object import InlineKeyboard
from aiogram.filters import and_f, or_f, Command
from .....keyboards.Text import Txt
from ....callbacks import models
from .....filters import isAdmin
from ....object import Commands
from .....routers import admin
from aiogram import types, F


@admin.message(
    and_f(or_f(F.text == Txt.EDIT, Command(Commands.edit)), isAdmin())
)
async def select_type_to_edit(msg: types.Message):
    keyboard = InlineKeyboard()

    set_keywords = lambda x: {"type": x}
    await msg.answer(
        text="Виберіть що бажаєте відрегдагувати:",
        reply_markup=keyboard.get_buttons(
            [
                (Txt.EXESIZES, models.SelectEditType, set_keywords(Txt.EXESIZES)),
                (Txt.RECOMENDATIONS, models.SelectEditType, set_keywords(Txt.RECOMENDATIONS)),
                (Txt.TYPETRAINYNGS, models.SelectEditType, set_keywords(Txt.TYPETRAINYNGS)),
                (Txt.CANCEL, models.DeleteCallbackMsg, {})
            ], 1
        )
    )
