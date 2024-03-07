from .....keyboards.Text import txtranslate, TranslateString
from .....keyboards.Reply import confirm_btns, admin_btns
from aiogram.utils.chat_action import ChatActionSender
from .....keyboards.Inline import inline_pagination
from .....models import ModelDataManipulation
from aiogram.fsm.context import FSMContext
from ....callbacks import models as clbks
from .....FSM import models as fsm
from aiogram.filters import and_f
from .....routers import admin
from aiogram import types, F


@admin.callback_query(
    clbks.DeleteCategory.filter()
)
async def start_delete_category_context(callback: types.CallbackQuery, callback_data: clbks.DeleteCategory):
    model, page, language = callback_data.type, callback_data.page, callback_data.lang

    data = ModelDataManipulation(model)

    get, total = await data.get_data_pagination(page=page)

    set_keywords = lambda: {"type": model, "lang": language}
    await callback.message.edit_text(
        text=await TranslateString(
            f"Для видалення категорії з {model} просто натисніть на неї:"
        ).translate_to_lang(language),
        reply_markup=inline_pagination(
            data=get,
            data_model=clbks.Delete,
            data_data=set_keywords(),
            prev_model=clbks.DeleteCategory,
            prev_data=set_keywords(),
            page=page,
            total_pages=total,
            cancel_txt=await txtranslate.BACK.translate_to_lang(language),
            cancel_model=clbks.EditCategory,
            cancel_data=set_keywords(),
        )
    )

@admin.callback_query(
    clbks.Delete.filter()
)
async def data_delete(callback: types.CallbackQuery, callback_data: clbks.Delete, state: FSMContext):
    model, identity, language = callback_data.type, callback_data.identity, callback_data.lang

    async with ChatActionSender.typing(
        bot=callback.bot,
        chat_id=callback.message.chat.id,
    ):
        await state.set_state(fsm.ConfirmDelete.identity)
        await state.update_data(type=model, identity=identity)

        await callback.message.delete()
        await callback.bot.send_message(
            chat_id=callback.message.chat.id,
            text=await TranslateString(
                f"Підтверідть видалення з {model}:"
            ).translate_to_lang(language),
            reply_markup=confirm_btns
        )



@admin.message(
        and_f(fsm.ConfirmDelete.identity, F.text == txtranslate.CONFIRM)
)
async def confirm_delete_data(msg: types.Message, state: FSMContext):
    async with ChatActionSender.typing(
        chat_id=msg.chat.id,
        bot=msg.bot
    ):
        data = await state.get_data()
        await state.clear()

        type, identity = data.get("type"), data.get("identity")

        model = ModelDataManipulation(type)

        _, message = await model.delete_data(exp=model.table.id == identity)

        await msg.answer(
            text=await TranslateString(message).translate_to_lang(
                msg.from_user.language_code
            ),
            reply_markup=admin_btns
        )


@admin.message(
    and_f(fsm.ConfirmDelete.identity, F.text == txtranslate.CANCEL_TXT)
)
async def cancel_delete(msg: types.Message, state: FSMContext):
    async with ChatActionSender.typing(
        bot=msg.bot,
        chat_id=msg.chat.id,
    ):
        await state.clear()
        await msg.answer(
            text=await TranslateString("Скасовано.").translate_to_lang(
                msg.from_user.language_code
            ),
            reply_markup=admin_btns
        )



@admin.message(
    fsm.ConfirmDelete.identity
)
async def not_correct_answer(msg: types.Message):
    await msg.answer(
        text=await TranslateString("Виберіть один із варіантів нижче:").translate_to_lang(
            msg.from_user.language_code
        ),
        reply_markup=confirm_btns
    )