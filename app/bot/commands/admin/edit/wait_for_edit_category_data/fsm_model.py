from app.bot.keyboards.Text.object import EditBtnTxt
from aiogram.fsm.state import State, StatesGroup
from typing import Literal


class AddFormCategory(StatesGroup):
    type: str = State()
    category: str = State()

class ConfirmDelete(StatesGroup):
    type: str = State()
    identity: int = State()
    confirm: str = State()