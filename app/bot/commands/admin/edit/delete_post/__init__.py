from .....keyboards.Reply import confirm_btns, admin_btns
from aiogram.utils.chat_action import ChatActionSender
from .....keyboards.Inline import inline_pagination
from .....models import ModelDataManipulation
from aiogram.fsm.context import FSMContext
from ....callbacks import models as clbks
from .....keyboards.Text import Txt
from .....FSM import models as fsm
from aiogram.filters import and_f
from .....routers import admin
from aiogram import types, F


@admin.callback_query(
    clbks.SelectCategoryForPostDelete.filter()
)
async def select_category_from_post_del(callback: types.CallbackQuery, callback_data: clbks.SelectCategoryForPostDelete):
    model, page = callback_data.type, callback_data.page

    category = ModelDataManipulation(model)

    get, total = await category.get_data_pagination(page=page)

    set_keywords = lambda x: {"type": x}
    await callback.message.edit_text(
        text=f"Виберіть категорію з якої бажаєте видалити пост в {model}:",
        reply_markup=inline_pagination(
            data=get,
            data_model=clbks.SelectPostToDelete,
            data_data=set_keywords(model),
            prev_model=clbks.SelectCategoryForPostDelete,
            prev_data=set_keywords(model),
            cancel_txt=Txt.BACK,
            cancel_model=clbks.EditPost,
            cancel_data=set_keywords(model),
            page=page,
            total_pages=total
        )
    )

@admin.callback_query(
    clbks.SelectPostToDelete.filter()
)
async def select_post_to_delete(callback: types.CallbackQuery, callback_data: clbks.SelectPostToDelete):
    model, identity, page = callback_data.type, callback_data.identity, callback_data.page

    category = ModelDataManipulation(model)
    posts = ModelDataManipulation(model, media=True)

    category = await category.async_get_where(category.table, exp=category.table.id == identity, all_=False)

    get, total = await posts.get_data_pagination(page=page, exp=posts.table.type == category.type, get_all=False)

    await callback.message.edit_text(
        text=f"Виберіть пост який бажаєте видалити з {category.type} в {model}:",
        reply_markup=inline_pagination(
            data=get,
            data_model=clbks.DeletePost,
            data_data={"type": model, "category": category.id},
            prev_model=clbks.SelectPostToDelete,
            prev_data={"type": model, "identity": identity},
            cancel_txt=Txt.BACK,
            cancel_model=clbks.SelectCategoryForPostDelete,
            cancel_data={"type": model},
            page=page,
            total_pages=total
        )
    )


@admin.callback_query(
    clbks.DeletePost.filter()
)
async def confirm_post_delete(callback: types.CallbackQuery, callback_data: clbks.DeletePost, state: FSMContext):
    async with ChatActionSender.typing(
        chat_id=callback.message.chat.id,
        bot=callback.bot
    ):
        model, category, identity = callback_data.type, callback_data.category, callback_data.identity

        await state.set_state(fsm.ConfirmPostDelete.post)
        await state.update_data(type=model, category=category, post=identity)

        await callback.message.delete()
        await callback.bot.send_message(
            chat_id=callback.message.chat.id,
            text="Підтвердіть видалення посту:",
            reply_markup=confirm_btns
        )


@admin.message(
        and_f(fsm.ConfirmPostDelete.post, F.text == Txt.CONFIRM)
)
async def confirm_to_delete_post(msg: types.Message, state: FSMContext):
    async with ChatActionSender.typing(
        chat_id=msg.chat.id,
        bot=msg.bot
    ):
        data = await state.get_data()

        model: str = data.get("type")
        category: int = data.get("category")
        post: int = data.get("post")

        get_category = ModelDataManipulation(model)
        get_category = await get_category.async_get_where(
            get_category.table, exp=get_category.table.id == category, all_=False
        )

        get_post_table = ModelDataManipulation(model, media=True)

        _, message = await get_post_table.delete_data(and__=(
            get_post_table.table.id == post,
            get_post_table.table.type == get_category.type
        ))

        await msg.answer(
            text=message,
            reply_markup=admin_btns
        )
        



@admin.message(
    and_f(fsm.ConfirmPostDelete.post, F.text == Txt.CANCEL_TXT)
)
async def cancel_post_delete(msg: types.Message, state: FSMContext):
    async with ChatActionSender.typing(
        chat_id=msg.chat.id,
        bot=msg.bot
    ):
        await state.clear()

        await msg.answer(
            text="Скасовано.",
            reply_markup=admin_btns
        )

@admin.message(
    fsm.ConfirmPostDelete.post
)
async def not_correct_answer_conf_post_delete(msg: types.Message):
    await msg.answer(
        text="Виберіть один з варіантів нижче",
        reply_markup=confirm_btns
    )