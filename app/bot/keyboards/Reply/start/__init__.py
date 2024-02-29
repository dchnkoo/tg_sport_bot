from aiogram.utils.keyboard import ReplyKeyboardBuilder
from app.bot.keyboards.Text.object import AdminEditBtnTxt


class StartButtons(ReplyKeyboardBuilder,
                   AdminEditBtnTxt):

    def get_buttons(self):
        self.button(text=self.adminbtn)
        return self.as_markup(resize_keyboard=True)