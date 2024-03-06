from ....keyboards.Inline import inline_pagination
from ....models import ModelDataManipulation
from aiogram.filters import Command, or_f
from ...callbacks import models as clbks
from ....keyboards.Text import Txt
from ...object import Commands
from ....routers import user
from aiogram import types


async def category_list_handler(msg: types.Message, model: str, page: int, callback: bool = False):
    category = ModelDataManipulation(model)

    get, total = await category.get_data_pagination(page=page)

    answer = inline_pagination(
        data=get,
        data_model=clbks.PostFromCategorySelect,
        data_data={"type": model},
        prev_model=clbks.UserChooseCategory,
        prev_data={"type": model},
        cancel_txt=Txt.CANCEL,
        cancel_model=clbks.DeleteCallbackMsg,
        cancel_data={"delete": True},
        page=page,
        total_pages=total
    )

    text = f"Виберіть категорію з якої бажаєте переглянути пост в {model}"

    await msg.edit_text(text=text, reply_markup=answer) if callback else await msg.answer(text=text, reply_markup=answer)



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
    model, page = callback_data.type, callback_data.page

    await category_list_handler(callback.message, model, page, callback=True)