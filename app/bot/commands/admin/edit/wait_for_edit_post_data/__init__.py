from app.bot.keyboards.Inline.admin.edit_callback import AdminKeyboardAddPostSelectCategory
from ..wait_for_edit_category_data.get_data_with_pagination import get_category_with_pages
from ..wait_for_edit_category_data.insert_category import get_correct_table
from app.bot.keyboards.Reply.cancel import CancelReplyButton, CancleBtns
from app.bot.keyboards.Text.object import EditBtnTxt, StartButtonsTxt
from app.bot.keyboards.CallbackModels.admin import AddCallbackData
from app.bot.keyboards.Reply.start import StartButtons
from app.database.model.asyncc import async_db

from aiogram.fsm.context import FSMContext
from .....routers.admin import admin
from .fsm_models import PostForm
from aiogram.filters import or_f
from aiogram import types, F



@admin.callback_query(
    AddCallbackData.filter(F.type.startswith(EditBtnTxt.post))
)
async def wait_for_post_data(callback: types.CallbackQuery, callback_data: AddCallbackData):
    data = callback_data.type.removeprefix(EditBtnTxt.post)

    type = StartButtonsTxt.get_attr(data)
    page = int(data.removeprefix(type))

    get = await get_correct_table(get_category_with_pages, **{"type": type, "page": page})

    keyboard = AdminKeyboardAddPostSelectCategory()

    await callback.message.edit_text(
        text=f"Виберіть категорію для якої бажаєте додати пост в {type}", 
        reply_markup=keyboard.get_buttons(get[0], get[1], page, EditBtnTxt.post + type)
    )


@admin.callback_query(
    AddCallbackData.filter(
            F.type.startswith(StartButtonsTxt.exesizes) |
            F.type.startswith(StartButtonsTxt.recomendations) |
            F.type.startswith(StartButtonsTxt.typetrainigs)
    )
)
async def start_context_to_add_post(callback: types.CallbackQuery, callback_data: AddCallbackData, state: FSMContext):
    # get type and id
    type = StartButtonsTxt.get_attr(callback_data.type)
    identificator = int(callback_data.type.removeprefix(type))

    # get table object
    object = await get_correct_table(None, only_table=True, type=type)

    # get category from table
    db = async_db()
    category = await db.async_get_where(object, exp=object.id == identificator, 
                             all_=False)
    category = category[0]

    await state.set_state(PostForm.title)
    await state.update_data(type=category.type)

    keyboard = CancelReplyButton()
    await callback.message.delete()
    await callback.bot.send_message(
        chat_id=callback.message.chat.id,
        text=f"Категорія: {category.type}\nВведіть заголовок для посту:",
        reply_markup=keyboard.get_buttons()
    )


@admin.message(
        or_f(PostForm.title, PostForm.media, PostForm.text, PostForm.buttons), 
        F.text == CancleBtns.cancel
)
async def cancel_context_to_add_post(msg: types.Message, state: FSMContext):

    current_state = await state.get_state()
    if current_state is None:
        return
    
    await state.clear()

    keyboard = StartButtons().get_buttons()
    await msg.answer(
        text="Скасовано.",
        reply_markup=keyboard
    )


@admin.message(PostForm.title)
async def get_title_context(msg: types.Message, state: FSMContext):

    data = await state.update_data(title=msg.text)
    await state.set_state(PostForm.media)

    await msg.answer(
        text=f"Категорія: {data.get('type')}\nЗаголовок: {data.get('title')}\n\nВідправте до 9 Фото/Відео:"
    )