from aiogram.utils.keyboard import ReplyKeyboardBuilder
from typing import List, Dict, Any


class ReplyKeyboard(ReplyKeyboardBuilder):

    def get_buttons(
            self,
            data: List[Dict[str, Any]],
            *adjust
    ):
        [self.button(**kwargs) for kwargs in data]

        self.adjust(*adjust) if adjust else None
        return self.as_markup(resize_keyboard=True)