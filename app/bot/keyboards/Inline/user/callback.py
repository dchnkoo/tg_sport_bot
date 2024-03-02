from aiogram.utils.keyboard import InlineKeyboardBuilder
from ...Text.object import CancleBtns
from typing import List, Tuple


class InlineSelectPagination(InlineKeyboardBuilder):
    

    def get_buttons(
                    
                    self, 
                    data: List[Tuple[int, str]], 
                    data_callback_model: object, 
                    data_callback_data: dict,
                    prev_model: object, 
                    prev_data: dict, 
                    page: int, 
                    total_pages: int, 
                    back_btn_model: object,
                    back_btn_data: dict,
                    back_to_cancel: bool = False

                ):
        
        [self.button(text=title, 
                    callback_data=data_callback_model(**data_callback_data, identity=identity))
                    for identity, title in data]

        self.button(text="<-", callback_data=prev_model(**{k: v - 1 if k == "page" else v for k,v in prev_data.items()})) if page > 1 else None
        self.button(text=CancleBtns.cancel if back_to_cancel else CancleBtns.back, callback_data=back_btn_model(**back_btn_data))
        self.button(text="->", callback_data=prev_model(**{k: v + 1 if k == "page" else v for k,v in prev_data.items()})) if page < total_pages else None

        self.adjust(*(*[1 for _ in data], 3))
        return self.as_markup()
