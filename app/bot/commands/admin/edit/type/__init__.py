from .....keyboards.Text import txtranslate, TranslateString
from .....keyboards.Inline.object import InlineKeyboard
from ....callbacks import models
from .....routers import admin
from aiogram import types


@admin.callback_query(
    models.SelectEditType.filter()
)
async def select_edit_type(callback: types.CallbackQuery, callback_data: models.SelectEditType):
    edit, language = callback_data.type, callback_data.lang

    keyboard = InlineKeyboard()
    
    set_keywords = lambda x: {"type": x, "lang": language}
    await callback.message.edit_text(

        text=await TranslateString(f"Виберіть що бажаєте відредагувати в {edit}:").translate_to_lang(language),

        reply_markup=keyboard.get_buttons(
            [
                (await txtranslate.TYPE.translate_to_lang(language), models.EditCategory, set_keywords(edit)),
                (await txtranslate.POST.translate_to_lang(language), models.EditPost, set_keywords(edit)),
                (txtranslate.CANCEL, models.DeleteCallbackMsg, {})

            ], 1
        )
    )

