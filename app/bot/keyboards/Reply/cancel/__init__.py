from aiogram.utils.keyboard import ReplyKeyboardBuilder
from app.bot.keyboards.Text.object import CancleBtns


class BackReplyButton(ReplyKeyboardBuilder):

    def get_buttons(self):
        self.button(text=CancleBtns.back)

        return self.as_markup(resize_keyboard=True)
    

class CancelReplyButton(ReplyKeyboardBuilder):

    def get_buttons(self):
        self.button(text=CancleBtns.cancel)

        return self.as_markup(resize_keyboard=True)