from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List, Tuple, Dict,Any


class InlineKeyboard(InlineKeyboardBuilder):

    def get_buttons(
            self,
            data: List[Tuple[str, object, Dict[str, Any]]],
            *adjust
    ):
        [self.button(text=text, callback_data=Model(**entites)) for text, Model, entites in data]

        self.adjust(*adjust) if adjust else None

        return self.as_markup()