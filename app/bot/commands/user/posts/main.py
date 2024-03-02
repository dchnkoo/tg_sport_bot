from ...admin.edit.wait_for_edit_category_data.get_data_with_pagination import get_patrition_data
from ...admin.edit.wait_for_edit_category_data.insert_category import get_correct_table
from ....keyboards.CallbackModels.user import UserCategory, UserPost, GetPost
from ....keyboards.Inline.user.callback import InlineSelectPagination
from aiogram.utils.chat_action import ChatActionSender
from app.bot.msg.builder import BuildTelegramMsg
from app.database.model.asyncc import async_db
from ....routers.user import user
from aiogram import types


@user.callback_query(
    UserPost.filter()
)
async def posts_list_callback(callback: types.CallbackQuery, callback_data: UserPost):
    type, page, identity = callback_data.type, callback_data.page, callback_data.identity

    table_media: object = await get_correct_table(None, only_table=True, media=True, type=type)
    table_type: object = await get_correct_table(None, only_table=True, type=type)

    async with ChatActionSender.typing(
        chat_id=callback.message.chat.id,
        bot=callback.bot
    ):
        db = async_db()

        category = await db.async_get_where(table_type.type, exp=table_type.id == identity,
                                            all_=False)
        
        data, total = await get_patrition_data(db, table_media, page=page, media_=True, 
                                               exp=table_media.type == category)

        keyboard = InlineSelectPagination()


        await callback.message.edit_text(
            text=f"Виберіть пост який бажаєте переглянути в {type}:",
            reply_markup=keyboard.get_buttons(
                data=data,
                data_callback_model=GetPost,
                data_callback_data={"type": type, "category_id": identity},
                page=page,
                total_pages=total,
                back_btn_model=UserCategory,
                back_btn_data={"type": type, "page": 1},
                prev_model=UserPost,
                prev_data={"type": type, "page": page, "identity": identity}
            )
        )


@user.callback_query(
    GetPost.filter()
)
async def send_post_to_user(callback: types.CallbackQuery, callback_data: GetPost):
    type, category_id, identity = callback_data.type, callback_data.category_id, callback_data.identity

    table_media: object = await get_correct_table(None, only_table=True, media=True, type=type)
    table_type: object = await get_correct_table(None, only_table=True, type=type)

    async with ChatActionSender.typing(
        chat_id=callback.message.chat.id,
        bot=callback.bot
    ):
        db = async_db()
        
        category = await db.async_get_where(table_type.type, exp=table_type.id == category_id,
                                            all_=False)
        
        post = await db.async_get_where(table_media, and__=(table_media.type == category, table_media.id == identity),
                                        all_=False)
        
        msg = BuildTelegramMsg(
            title=post.title,
            media=post.media,
            text=post.text,
            buttons=post.buttons,
            type=post.type
        )

    await callback.message.delete()
    await callback.message.answer_media_group(
        msg.get_media_group(decode=True)
    )
    await callback.message.answer(**msg.get_msg())