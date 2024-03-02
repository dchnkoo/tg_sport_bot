from aiogram.fsm.state import State, StatesGroup
from typing import List, Tuple


class PostForm(StatesGroup):
    title: str = State()
    media: List[Tuple[str, str]] = State()
    type: str = State()
    text: str = State()
    buttons: List[List[Tuple[str, str]]] = State()

    object_db: object = State()
    category: str = State()
    confirm = State()

class ConfirmPostDelete(StatesGroup):
    identity: str = State()
    table: object = State()