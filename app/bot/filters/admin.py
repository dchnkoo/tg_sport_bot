from aiogram.filters import Filter
from aiogram import types

from app.settings import ADMIN


class isAdmin(Filter):

    async def __call__(self, msg: types.Message) -> bool: 
        if msg.from_user.id == ADMIN:
            return True
        return False