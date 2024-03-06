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
    clbks.DeleteCategory.filter()
)
async def start_delete_category_context(callback: types.CallbackQuery, callback_data: clbks.DeleteCategory):
    model, page = callback_data.type, callback_data.page

    data = ModelDataManipulation(model)

    get, total = await data.get_data_pagination(page=page)

    await callback.message.edit_text(
        text=f"Для видалення категорії з {model} просто натисніть на неї:",
        reply_markup=inline_pagination(
            data=get,
            data_model=clbks.Delete,
            data_data={"type": model},
            prev_model=clbks.DeleteCategory,
            prev_data={"type": model},
            page=page,
            total_pages=total,
            cancel_txt=Txt.BACK,
            cancel_model=clbks.EditCategory,
            cancel_data={"type": model},
        )
    )

@admin.callback_query(
    clbks.Delete.filter()
)
async def data_delete(callback: types.CallbackQuery, callback_data: clbks.Delete, state: FSMContext):
    model, identity = callback_data.type, callback_data.identity

    async with ChatActionSender.typing(
        bot=callback.bot,
        chat_id=callback.message.chat.id,
    ):
        await state.set_state(fsm.ConfirmDelete.identity)
        await state.update_data(type=model, identity=identity)

        await callback.message.delete()
        await callback.bot.send_message(
            chat_id=callback.message.chat.id,
            text=f"Підтверідть видалення з {model}:",
            reply_markup=confirm_btns
        )



@admin.message(
        and_f(fsm.ConfirmDelete.identity, F.text == Txt.CONFIRM)
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
            text=message,
            reply_markup=admin_btns
        )


@admin.message(
    and_f(fsm.ConfirmDelete.identity, F.text == Txt.CANCEL_TXT)
)
async def cancel_delete(msg: types.Message, state: FSMContext):
    async with ChatActionSender.typing(
        bot=msg.bot,
        chat_id=msg.chat.id,
    ):
        await state.clear()
        await msg.answer(
            text="Скасовано.",
            reply_markup=admin_btns
        )



@admin.message(
    fsm.ConfirmDelete.identity
)
async def not_correct_answer(msg: types.Message):
    await msg.answer(
        text="Виберіть один із варіантів нижче:",
        reply_markup=confirm_btns
    )