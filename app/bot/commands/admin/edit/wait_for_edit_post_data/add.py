from ..wait_for_edit_category_data.insert_category import get_correct_table
from app.bot.keyboards.Reply.cancel import CancelReplyButton
from aiogram.utils.chat_action import ChatActionSender
from app.bot.keyboards.Reply.start import StartButtons
from app.bot.keyboards.Text.object import EditBtnTxt
from app.database.model.asyncc import async_db
from aiogram.fsm.context import FSMContext
from .....routers.admin import admin
from .fsm_models import PostForm
from app.settings import logger
from aiogram import types, F
import base64


@admin.message(PostForm.confirm, F.text == EditBtnTxt.confirm)
async def confirm_add_post_to_db(msg: types.Message, state: FSMContext):
    data: dict = await state.get_data()

    category = data.pop("category")
    data.pop("confirm", None)
    data.pop("object_db", None)
    table = await get_correct_table(None,  media=True, only_table=True, type=category)

    async with ChatActionSender.typing(
        chat_id=msg.chat.id, 
        bot=msg.bot
    ):
        media = data.get("media")
        data.update(media=[[content, base64.b64encode(value).decode("utf-8")] for content, value in media])
        
        db = async_db()
        keyboard = StartButtons()

        try: await db.async_insert_data(table, get_data=False, **data)
        except Exception as e:
            logger.error(f"file: {__file__}\nfunc: {confirm_add_post_to_db.__name__}\nError: {e}")

            await msg.answer(
                text="Помилка під час додавання данних. Спробуйте ще раз",
                reply_markup=keyboard.get_buttons()
            )

        else:
            await msg.answer(
                text=f"Пост для категорії {data.get('type')} був успішно доданий!",
                reply_markup=keyboard.get_buttons()
            )

        finally:
            await state.clear()


@admin.message(PostForm.confirm, ~F.text | F.text)
async def not_correct_context(msg: types.Message):
    keyboard = CancelReplyButton()
    await msg.answer(
        text="Виберіть один з варіантів наведених нижче.",
        reply_markup=keyboard.get_buttons(confirm=True)
    )