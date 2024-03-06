from .....routers import admin
from ....callbacks import models
from aiogram import types


@admin.callback_query(
    models.DeleteCallbackMsg.filter()
)
async def delete_callback_msg(callback: types.CallbackQuery):
    await callback.message.delete()