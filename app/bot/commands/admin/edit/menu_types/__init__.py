from .....keyboards.Text import txtranslate, TranslateString
from app.bot.keyboards.Inline.object import InlineKeyboard
from aiogram.filters import and_f, or_f, Command
from ....callbacks import models
from .....filters import isAdmin
from ....object import Commands
from .....routers import admin
from aiogram import types, F


@admin.message(
    and_f(or_f(F.text == txtranslate.EDIT, Command(Commands.edit)), isAdmin())
)
async def select_type_to_edit(msg: types.Message):
    keyboard = InlineKeyboard()
    language = msg.from_user.language_code

    set_keywords = lambda x: {"type": x, "lang": language}
    await msg.answer(
        text=await TranslateString("Виберіть що бажаєте відрегдагувати:").translate_to_lang(language),
        reply_markup=keyboard.get_buttons(
            [
                (
                    await txtranslate.EXESIZES.translate_to_lang(language),
                    models.SelectEditType, set_keywords(txtranslate.EXESIZES)
                ),
                (
                    await txtranslate.RECOMENDATIONS.translate_to_lang(language), 
                    models.SelectEditType, set_keywords(txtranslate.RECOMENDATIONS)
                ),
                (
                    await txtranslate.TYPETRAINYNGS.translate_to_lang(language), 
                    models.SelectEditType, set_keywords(txtranslate.TYPETRAINYNGS)
                ),
                (
                    txtranslate.CANCEL, 
                    models.DeleteCallbackMsg, {}
                )
            ], 1
        )
    )
