from aiogram.utils.chat_action import ChatActionSender
from ....keyboards.Inline import inline_pagination
from ....models import ModelDataManipulation
from ....msg.builder import BuildTelegramMsg
from ...callbacks import models as clbks
from ....keyboards.Text import Txt
from ....routers import user
from aiogram import types


@user.callback_query(
    clbks.PostFromCategorySelect.filter()
)
async def choose_post_user(callback: types.CallbackQuery, callback_data: clbks.PostFromCategorySelect):
    async with ChatActionSender.typing(
        chat_id=callback.message.chat.id,
        bot=callback.bot
    ):
        model, identity, page = callback_data.type, callback_data.identity, callback_data.page

        # get category
        category = ModelDataManipulation(model)
        category = await category.async_get_where(category.table, exp=category.table.id == identity, all_=False)

        media_data = ModelDataManipulation(model, media=True)
        get, total = await media_data.get_data_pagination(exp=media_data.table.type == category.type, get_all=False, page=page)

        await callback.message.edit_text(
            text=f"Виберіть пост який бажаєте переглянути для {model} в категорії {category.type}:",
            reply_markup=inline_pagination(
                data=get,
                data_model=clbks.GetUserPost,
                data_data={"type": model, "category": category.id},
                prev_model=clbks.PostFromCategorySelect,
                prev_data={"type": model, "identity": identity},
                cancel_txt=Txt.BACK,
                cancel_model=clbks.UserChooseCategory,
                cancel_data={"type": model},
                page=page,
                total_pages=total
            )
        )


@user.callback_query(
    clbks.GetUserPost.filter()
)
async def send_post_to_user(callback: types.CallbackQuery, callback_data: clbks.GetUserPost):
    async with ChatActionSender.typing(
        chat_id=callback.message.chat.id,
        bot=callback.bot
    ):
        model, category_id, post_id = callback_data.type, callback_data.category, callback_data.identity

        category = ModelDataManipulation(model)
        category = await category.async_get_where(category.table, exp=category.table.id == category_id, all_=False)

        media = ModelDataManipulation(model, media=True)
        media = await media.async_get_where(media.table, and__=(media.table.id == post_id, media.table.type == category.type), all_=False)

        message = BuildTelegramMsg(
            title=media.title,
            media=media.media,
            text=media.text,
            buttons=media.buttons,
            type=media.type
        )

        await callback.message.delete()
        
        if media.media: 
            await callback.bot.send_media_group(
                chat_id=callback.message.chat.id,
                media=message.get_media_group(decode=True),
            )
        await callback.bot.send_message(
            chat_id=callback.message.chat.id,
            **message.get_msg()
        )