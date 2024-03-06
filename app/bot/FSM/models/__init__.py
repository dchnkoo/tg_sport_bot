from typing import List, Tuple
from aiogram.fsm.state import State, StatesGroup


class AddCategoryState(StatesGroup):
    type: str = State()
    category: str = State()

class ConfirmDelete(StatesGroup):
    type: str = State()
    identity: int = State()

class AddPostState(StatesGroup):
    title: str = State()
    media: List[Tuple[str, str]] = State()
    type: str = State()
    text: str = State()
    buttons: List[List[Tuple[str, str]]] = State()

    category: str = State()
    confirm: str = State()

class ConfirmPostDelete(StatesGroup):
    type: str = State()
    category: str = State()
    post: int = State()