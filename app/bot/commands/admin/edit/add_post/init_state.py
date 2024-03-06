from aiogram.utils.chat_action import ChatActionSender
from .....keyboards.Inline import inline_pagination
from .....models import ModelDataManipulation
from .....keyboards.Reply import cancel_btns
from aiogram.fsm.context import FSMContext 
from ....callbacks import models as clbks
from .....keyboards.Text import Txt
from .....FSM import models as fsm
from .....routers import admin
from aiogram import types


@admin.callback_query(
    clbks.SelectCategoryForPostAdd.filter()
)
async def start_add_post_context(callback: types.CallbackQuery, callback_data: clbks.SelectCategoryForPostAdd):
        model, page = callback_data.type, callback_data.page

        async with ChatActionSender.typing(
             bot=callback.bot,
             chat_id=callback.message.chat.id
        ):
            manip = ModelDataManipulation(model)

            get, total = await manip.get_data_pagination(page=page)

            set_keywords = lambda x: {"type": x}
            await callback.message.edit_text(
                text=f"Виберіть категорію в яку хочете додати пост в {model}:",
                reply_markup=inline_pagination(
                    data=get,
                    data_model=clbks.AddPost,
                    data_data=set_keywords(model),
                    prev_model=clbks.SelectCategoryForPostAdd,
                    prev_data=set_keywords(model),
                    cancel_txt=Txt.BACK,
                    cancel_model=clbks.EditPost,
                    cancel_data=set_keywords(model),
                    page=page,
                    total_pages=total
                )
            )


@admin.callback_query(
        clbks.AddPost.filter()
)
async def start_add_post_context(callback: types.CallbackQuery, callback_data: clbks.AddPost, state: FSMContext):
    model, identity = callback_data.type, callback_data.identity

    async with ChatActionSender.typing(
        bot=callback.bot,
        chat_id=callback.message.chat.id,
    ):
        get_category = ModelDataManipulation(model)

        category = await get_category.async_get_where(get_category.table, exp=get_category.table.id == identity,
                                     all_=False)
        
        await state.set_state(fsm.AddPostState.title)
        await state.update_data(type=category.type, category=model,
                                buttons=[], media=[])

        await callback.message.delete()
        await callback.bot.send_message(
            chat_id=callback.message.chat.id,
            text=f"Введіть заголовок для посту в {model}",
            reply_markup=cancel_btns
        )