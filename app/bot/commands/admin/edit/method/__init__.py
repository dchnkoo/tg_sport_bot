from .....keyboards.Text import txtranslate, TranslateString
from .....keyboards.Inline.object import InlineKeyboard
from ....callbacks import models
from .....routers import admin
from aiogram import types


set_keywords = lambda x, lang: {"type": x, "lang": lang}

@admin.callback_query(
    models.EditCategory.filter()
)
async def select_edit_method_category(callback: types.CallbackQuery, callback_data: models.EditCategory):
    model, language = callback_data.type, callback_data.lang

    keyboard = InlineKeyboard()

    await callback.message.edit_text(
        text=await TranslateString(f"Що бажаєте зробити для {txtranslate.TYPE} в {model}?").translate_to_lang(language),
        reply_markup=keyboard.get_buttons(
            [
                (await txtranslate.ADD.translate_to_lang(language), models.AddCategory, set_keywords(model, language)),
                (await txtranslate.DELETE.translate_to_lang(language), models.DeleteCategory, set_keywords(model, language)),
                (await txtranslate.BACK.translate_to_lang(language), models.SelectEditType, set_keywords(model, language))
            ], 1
        )
    )


@admin.callback_query(
    models.EditPost.filter()
)
async def select_edit_method_post(callback: types.CallbackQuery, callback_data: models.EditPost):
    model, language = callback_data.type, callback_data.lang

    keyboard = InlineKeyboard()

    await callback.message.edit_text(
        text=await TranslateString(f"Що бажаєте зробити для {txtranslate.POST} в {model}?").translate_to_lang(language),
        reply_markup=keyboard.get_buttons(
            [
                (await txtranslate.ADD.translate_to_lang(language), models.SelectCategoryForPostAdd, set_keywords(model, language)),
                (await txtranslate.DELETE.translate_to_lang(language), models.SelectCategoryForPostDelete, set_keywords(model, language)),
                (await txtranslate.BACK.translate_to_lang(language), models.SelectEditType, set_keywords(model, language))
            ], 1
        )
    )