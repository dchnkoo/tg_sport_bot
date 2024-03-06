from .object import InlineKeyboard
from typing import Tuple, List


def inline_pagination(
        data: List[Tuple[int, str]],
        data_model: object,
        data_data: dict,
        prev_model: object,
        prev_data: dict,
        cancel_txt: str,
        cancel_model: object,
        cancel_data: dict,
        page: int,
        total_pages: int,
):
    keyboard = InlineKeyboard()

    data_list = [(text, data_model, data_data | {"identity": identity}) for identity, text in data]


    data_list.append(("<--", prev_model, prev_data | {"page": page - 1})) if page > 1 else None
    data_list.append((cancel_txt, cancel_model, cancel_data))
    data_list.append(("-->", prev_model, prev_data | {"page": page + 1})) if page < total_pages else None

    return keyboard.get_buttons(
        data_list,
        *[*[1 for _ in data], 3]
    )

