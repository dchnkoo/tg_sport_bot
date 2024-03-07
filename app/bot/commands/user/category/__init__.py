from ....keyboards.Text import txtranslate, TranslateString
from ....keyboards.Inline import inline_pagination
from ....models import ModelDataManipulation
from aiogram.filters import Command, or_f
from ...callbacks import models as clbks
from ...object import Commands
from ....routers import user
from aiogram import types


async def category_list_handler(msg: types.Message, model: str, page: int, lang: str = None):
    category = ModelDataManipulation(model)

    get, total = await category.get_data_pagination(page=page)
    language = lang if lang else msg.from_user.language_code 

    set_keywords = lambda: {"type": model, "lang": language}
    answer = inline_pagination(
        data=get,
        data_model=clbks.PostFromCategorySelect,
        data_data=set_keywords(),
        prev_model=clbks.UserChooseCategory,
        prev_data=set_keywords(),
        cancel_txt=await txtranslate.CANCEL.translate_to_lang(language),
        cancel_model=clbks.DeleteCallbackMsg,
        cancel_data={"delete": True},
        page=page,
        total_pages=total
    )

    text = await TranslateString(
        f"Виберіть категорію з якої бажаєте переглянути пост в {model}"
    ).translate_to_lang(language)
    
    await msg.edit_text(text=text, reply_markup=answer) if lang else await msg.answer(text=text, reply_markup=answer)



@user.message(
        or_f(
            Command(Commands.EXESIZES),
            Command(Commands.RECOMENDATIONS),
            Command(Commands.TYPETRAINYNGS)
        )
)
async def select_category_user(msg: types.Message):
    model, page = Commands.get_command_type(msg.text.removeprefix("/")), 1

    await category_list_handler(msg, model, page)


@user.callback_query(
    clbks.UserChooseCategory.filter()
)
async def user_choose_category(callback: types.CallbackQuery, callback_data: clbks.UserChooseCategory):
    model, page, language = callback_data.type, callback_data.page, callback_data.lang

    await category_list_handler(callback.message, model, page, language)