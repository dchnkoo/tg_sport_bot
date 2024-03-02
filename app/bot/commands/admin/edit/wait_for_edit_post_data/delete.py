from ..wait_for_edit_category_data.get_data_with_pagination import get_category_with_pages
from app.bot.keyboards.Inline.admin.edit_callback import AdminKeyboardDeleteSelectPost
from .....keyboards.CallbackModels.admin import DeleteCallbackData, ConfirmDeletePost
from ..wait_for_edit_category_data.insert_category import get_correct_table
from app.bot.keyboards.Text.object import EditBtnTxt, StartButtonsTxt
from .....keyboards.Reply.confirm import ConfirmButtons
from aiogram.utils.chat_action import ChatActionSender  
from .....keyboards.Reply.start import StartButtons
from app.database.model.asyncc import async_db
from aiogram.fsm.context import FSMContext
from .fsm_models import ConfirmPostDelete
from .....routers.admin import admin
from aiogram.filters import and_f
from app.settings import logger
from aiogram import types, F


@admin.callback_query(
    DeleteCallbackData.filter(F.type.startswith(EditBtnTxt.post))
)
async def start_delete_state_post(callback: types.CallbackQuery, callback_data: DeleteCallbackData):
    data = callback_data.type.removeprefix(EditBtnTxt.post)
    category = StartButtonsTxt.get_attr(data)
    page = int(data.removeprefix(category))

    async with ChatActionSender.typing(
        bot=callback.bot,
        chat_id=callback.message.chat.id
    ):
        data = await get_correct_table(get_category_with_pages, media=True, media_=True, page=page, type=category)

        keyboard = AdminKeyboardDeleteSelectPost()
        
        await callback.message.edit_text(
            text=f"Для видалення {EditBtnTxt.post} в {category} натисніть на кнопку з відповідним заголовоком:",
            reply_markup=keyboard.get_buttons(data[0], category, callback_data=EditBtnTxt.post + category, page=page, total_pages=data[1])
        )


@admin.callback_query(
    ConfirmDeletePost.filter()
)
async def confirm_post_delete(callback: types.CallbackQuery, callback_data: ConfirmDeletePost, state: FSMContext):
    category = callback_data.type
    identity = callback_data.identity

    async with ChatActionSender.typing(
        bot=callback.bot,
        chat_id=callback.message.chat.id
    ):
        await state.set_state(ConfirmPostDelete.identity)

        table = await get_correct_table(None, media=True, only_table=True, type=category)

        await state.update_data(table=table)

        db = async_db()

        data = await db.async_get_where(table, exp=table.id == identity, all_=False)

        await state.update_data(identity=data.id)
        
        keyboard = ConfirmButtons()
        await callback.message.delete()
        await callback.message.answer(
            text=f"Точно бажаєте видалити {EditBtnTxt.post} '{data.title}' з {category}?",
            reply_markup=keyboard.get_buttons()
        )


@admin.message(and_f(ConfirmPostDelete.identity, F.text == EditBtnTxt.confirm))
async def confirm_delete_post(msg: types.Message, state: FSMContext):

    async with ChatActionSender.typing(
        bot=msg.bot,
        chat_id=msg.chat.id,
    ):
        data: dict = await state.get_data()
        identity = data.get("identity")
        table = data.get("table")

        db = async_db()

        keyboard = StartButtons()

        try: await db.async_delete_data(table, exp=table.id == identity)
        except Exception as e:
            logger.error(f"file: {__file__}\nfunc: {confirm_delete_post.__name__}\nError: {e}")
            
            await msg.answer(
                text="Щось пішло не так, спробуйте ще раз",
                reply_markup=keyboard.get_buttons()
            )

        else: 
            await msg.answer(
                text="Пост видалений!",
                reply_markup=keyboard.get_buttons()
            )

        finally:
            await state.clear()