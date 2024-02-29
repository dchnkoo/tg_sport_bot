from aiogram.fsm.state import State, StatesGroup
from typing import List, Tuple


class PostForm(StatesGroup):
    title: str = State()
    media: List[Tuple[str, str]] = State()
    type: str = State()
    text: str = State()
    buttons: List[List[Tuple[str, str]]] = State()