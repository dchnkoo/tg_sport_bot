from ..Text import Txt
from .object import ReplyKeyboard


set_keywords = lambda x: {"text": x}

admin_btns = ReplyKeyboard().get_buttons([set_keywords(Txt.EDIT)])

cancel_btns = ReplyKeyboard().get_buttons([set_keywords(Txt.CANCEL_TXT)])

confirm_btns = ReplyKeyboard().get_buttons([set_keywords(Txt.CONFIRM), set_keywords(Txt.CANCEL_TXT)])

def get_media_btns(skip: bool = False, go: bool = False):
    data = []

    data.append(set_keywords(Txt.GO)) if go else None
    data.append(set_keywords(Txt.SKIP)) if skip else None
    data.append(set_keywords(Txt.CANCEL_TXT))

    adjust = [1, 1] if len(data) == 2 else [2, 1]

    return ReplyKeyboard().get_buttons(data, *adjust)