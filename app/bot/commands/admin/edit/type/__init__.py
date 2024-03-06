from .....keyboards.Inline.object import InlineKeyboard
from .....keyboards.Text import Txt
from ....callbacks import models
from .....routers import admin
from aiogram import types


@admin.callback_query(
    models.SelectEditType.filter()
)
async def select_edit_type(callback: types.CallbackQuery, callback_data: models.SelectEditType):
    edit = callback_data.type

    keyboard = InlineKeyboard()

    set_keywords = lambda x: {"type": x}
    await callback.message.edit_text(
        text=f"Виберіть що бажаєте відредагувати в {edit}:",
        reply_markup=keyboard.get_buttons(
            [
                (Txt.TYPE, models.EditCategory, set_keywords(edit)),
                (Txt.POST, models.EditPost, set_keywords(edit)),
                (Txt.CANCEL, models.DeleteCallbackMsg, {})

            ], 1
        )
    )

