from aiogram.utils.keyboard import ReplyKeyboardBuilder
from app.bot.keyboards.Text.object import CancleBtns, EditBtnTxt


class BackReplyButton(ReplyKeyboardBuilder):

    def get_buttons(self):
        self.button(text=CancleBtns.back)

        return self.as_markup(resize_keyboard=True)
    

class CancelReplyButton(ReplyKeyboardBuilder):

    def get_buttons(self, skip: bool = False, go: bool = False, confirm: bool = False):
        self.button(text=CancleBtns.go) if go else None
        self.button(text=CancleBtns.skip) if skip else None
        self.button(text=EditBtnTxt.confirm) if confirm else None
        self.button(text=CancleBtns.cancel)

        self.adjust(2, 1) if skip and go else self.adjust(1, 1)
        return self.as_markup(resize_keyboard=True)