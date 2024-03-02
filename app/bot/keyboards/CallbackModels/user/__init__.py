from aiogram.filters.callback_data import CallbackData


class UserCategory(CallbackData, prefix="UC"):
    type: str
    page: int

class UserPost(CallbackData, prefix="UP"):
    type: str
    page: int
    identity: int


class GetPost(CallbackData, prefix="GP"):
    type: str
    category_id: int
    identity: int