from aiogram.filters.callback_data import CallbackData


class EditCallbackBtn(CallbackData, prefix="select_type"):
    type: str

class EditCallbackData(CallbackData, prefix="ed"):
    type: str

class AddCallbackData(CallbackData, prefix="add"):
    type: str

class DeleteCallbackData(CallbackData, prefix="del"):
    type: str

class AddPost(CallbackData, prefix="add-post"):
    type: str

class ConfirmDeletePost(CallbackData, prefix="p-del"):
    type: str
    identity: int