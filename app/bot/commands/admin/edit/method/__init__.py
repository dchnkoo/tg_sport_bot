from .....keyboards.Inline.object import InlineKeyboard
from .....keyboards.Text import Txt
from ....callbacks import models
from .....routers import admin
from aiogram import types


set_keywords = lambda x: {"type": x}

@admin.callback_query(
    models.EditCategory.filter()
)
async def select_edit_method_category(callback: types.CallbackQuery, callback_data: models.EditCategory):
    model = callback_data.type

    keyboard = InlineKeyboard()

    await callback.message.edit_text(
        text=f"Що бажаєте зробити для {Txt.TYPE} в {model}?",
        reply_markup=keyboard.get_buttons(
            [
                (Txt.ADD, models.AddCategory, set_keywords(model)),
                (Txt.DELETE, models.DeleteCategory, set_keywords(model)),
                (Txt.BACK, models.SelectEditType, set_keywords(model))
            ], 1
        )
    )


@admin.callback_query(
    models.EditPost.filter()
)
async def select_edit_method_post(callback: types.CallbackQuery, callback_data: models.EditPost):
    model = callback_data.type

    keyboard = InlineKeyboard()

    await callback.message.edit_text(
        text=f"Що бажаєте зробити для {Txt.POST} в {model}?",
        reply_markup=keyboard.get_buttons(
            [
                (Txt.ADD, models.SelectCategoryForPostAdd, set_keywords(model)),
                (Txt.DELETE, models.SelectCategoryForPostDelete, set_keywords(model)),
                (Txt.BACK, models.SelectEditType, set_keywords(model))
            ], 1
        )
    )