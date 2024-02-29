from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.bot.keyboards.Text.object import AdminEditBtnTxt as btns, CancleBtns
from app.bot.keyboards.CallbackModels.admin import EditCallbackBtn


class AdminEditKeyBoard(InlineKeyboardBuilder):

    def get_buttons(self):
        self.button(text=btns.exesizes, callback_data=EditCallbackBtn(type=btns.exesizes))
        self.button(text=btns.recomendations, callback_data=EditCallbackBtn(type=btns.recomendations))
        self.button(text=btns.typetrainigs, callback_data=EditCallbackBtn(type=btns.typetrainigs))
        self.button(text=CancleBtns.cancel, callback_data=EditCallbackBtn(type=CancleBtns.cancel))

        self.adjust(1)
        return self.as_markup()