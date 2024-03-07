from app.settings import BUTTONS_LIMIT
from ..language import TranslateString
from aiogram.filters import Filter
from app.settings import ADMIN
from ..regex import check_text
from aiogram import types


class isAdmin(Filter):

    async def __call__(self, msg: types.Message):
        return str(msg.from_user.id) in ADMIN
    

class isButtons(Filter):

    async def __call__(self, msg: types.Message):
        text = msg.text
        check = check_text(text)

        if len(check if check is not None else []) > BUTTONS_LIMIT:
            await msg.answer(
                text=await TranslateString(
                    f"Не можливо додати більше {BUTTONS_LIMIT} кнопок"
                ).translate_to_lang(msg.from_user.language_code)
            )
            return False
        elif text:
            return True
        else: return False