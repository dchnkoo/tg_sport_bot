from ...admin.edit.wait_for_edit_category_data.get_data_with_pagination import get_category_with_pages
from ...admin.edit.wait_for_edit_category_data.insert_category import get_correct_table
from ....keyboards.CallbackModels.user import UserCategory, UserPost
from ....keyboards.Inline.user.callback import InlineSelectPagination
from app.bot.keyboards.CallbackModels.admin import EditCallbackBtn
from aiogram.utils.chat_action import ChatActionSender
from app.bot.keyboards.Text.object import CancleBtns
from app.database.model.asyncc import async_db
from aiogram.filters import Command
from ...object import CommandsBot
from ....routers.user import user
from aiogram import types


async def category_list_handler(msg: types.Message, category, page: int, callback: bool = False):
    
    table = await get_correct_table(None, only_table=True, type=category)

    db = async_db()
    async with ChatActionSender.typing(
        bot=msg.bot,
        chat_id=msg.chat.id,
    ):
        data, total = await get_category_with_pages(db, table, page=page)

        keyboard = InlineSelectPagination()

    user_data_for_models = {"type": category, "page": page}

    answer = {
        "text": f"На яку тему бажаєте переглянути пост в {category}?",
        "reply_markup": keyboard.get_buttons(
            data, 
            page=page,
            total_pages=total,
            back_to_cancel=True,
            prev_model=UserCategory,
            data_callback_model=UserPost,
            prev_data=user_data_for_models,
            back_btn_model=EditCallbackBtn,
            data_callback_data=user_data_for_models,
            back_btn_data={"type": CancleBtns.cancel},
        )
    }

    await msg.edit_text(**answer) if callback else await msg.answer(**answer)


@user.message(Command(
        CommandsBot.EXESIZES.no_prefix,
        CommandsBot.RECOMENDATIONS.no_prefix,
        CommandsBot.TYPETRAININGS.no_prefix
))
async def get_exesizes_list_categories(msg: types.Message):
    category, page = CommandsBot.get_command_description(msg.text), 1

    await category_list_handler(msg, category, page)



@user.callback_query(
    UserCategory.filter()
)
async def categories_list_callback(callback: types.CallbackQuery, callback_data: UserCategory):
    category, page = callback_data.type, callback_data.page

    await category_list_handler(callback.message, category, page, callback=True)