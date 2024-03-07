from .....keyboards.Text import txtranslate, TranslateString
from aiogram.utils.chat_action import ChatActionSender
from .....keyboards.Inline import inline_pagination
from .....models import ModelDataManipulation
from .....keyboards.Reply import cancel_btns
from aiogram.fsm.context import FSMContext 
from ....callbacks import models as clbks
from .....FSM import models as fsm
from .....routers import admin
from aiogram import types


@admin.callback_query(
    clbks.SelectCategoryForPostAdd.filter()
)
async def start_add_post_context(callback: types.CallbackQuery, callback_data: clbks.SelectCategoryForPostAdd):
        model, page, language = callback_data.type, callback_data.page, callback_data.lang

        async with ChatActionSender.typing(
             bot=callback.bot,
             chat_id=callback.message.chat.id
        ):
            manip = ModelDataManipulation(model)

            get, total = await manip.get_data_pagination(page=page)

            set_keywords = lambda: {"type": model, "lang": language}
            await callback.message.edit_text(
                text=await TranslateString(
                     f"Виберіть категорію в яку хочете додати пост в {model}:"
                ).translate_to_lang(language),
                reply_markup=inline_pagination(
                    data=get,
                    data_model=clbks.AddPost,
                    data_data=set_keywords(),
                    prev_model=clbks.SelectCategoryForPostAdd,
                    prev_data=set_keywords(),
                    cancel_txt=await txtranslate.BACK.translate_to_lang(language),
                    cancel_model=clbks.EditPost,
                    cancel_data=set_keywords(),
                    page=page,
                    total_pages=total
                )
            )


@admin.callback_query(
        clbks.AddPost.filter()
)
async def start_add_post_context(callback: types.CallbackQuery, callback_data: clbks.AddPost, state: FSMContext):
    model, identity, language = callback_data.type, callback_data.identity, callback_data.lang

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
            text=await TranslateString(
                 f"Введіть заголовок для посту в {model}"
            ).translate_to_lang(language),
            reply_markup=cancel_btns
        )