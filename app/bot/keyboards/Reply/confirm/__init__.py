from aiogram.utils.keyboard import ReplyKeyboardBuilder
from app.bot.keyboards.Text.object import EditBtnTxt


class ConfirmButtons(ReplyKeyboardBuilder):

    def get_buttons(self):
        self.button(text=EditBtnTxt.confirm)
        self.button(text=EditBtnTxt.cancel)

        self.adjust(2)
        return self.as_markup(resize_keyboard=True)