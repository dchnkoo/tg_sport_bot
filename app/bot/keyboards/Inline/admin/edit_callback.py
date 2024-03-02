from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.bot.keyboards.Text.object import CancleBtns, EditBtnTxt
from app.bot.keyboards.CallbackModels.admin import (EditCallbackData, EditCallbackBtn,
                                                    AddCallbackData, DeleteCallbackData, ConfirmDeletePost)

from typing import List, Tuple


class AdminEditKeyBoardCallback(InlineKeyboardBuilder):

    def get_buttons(self, callback_data):
        self.button(text=EditBtnTxt.type, callback_data=EditCallbackData(type=EditBtnTxt.type + callback_data))
        self.button(text=EditBtnTxt.post, callback_data=EditCallbackData(type=EditBtnTxt.post + callback_data))
        self.button(text=CancleBtns.cancel, callback_data=EditCallbackBtn(type=CancleBtns.cancel))

        self.adjust(1)
        return self.as_markup()
    

class AdminEditKeyBoardCallbackData(InlineKeyboardBuilder):
        
        def get_buttons(self, callback_data: str):

            post = EditBtnTxt.post
            type = EditBtnTxt.type

            get_prefix = lambda: post if callback_data.startswith(post) else type
            cancel = callback_data.removeprefix(get_prefix())
            
            # if you want add post add number for start pagination pages
            to_posts = callback_data + "1" if get_prefix() == post else callback_data

            self.button(text=EditBtnTxt.add, callback_data=AddCallbackData(type=to_posts))
            self.button(text=EditBtnTxt.delete, callback_data=DeleteCallbackData(type=callback_data + "1"))
            self.button(text=CancleBtns.back, callback_data=EditCallbackBtn(type=cancel))

            self.adjust(1)
            return self.as_markup()
        

class AdminKeyBoardBackFromCallback(InlineKeyboardBuilder):
     
     def get_buttons(self, callback_data):
          self.button(text=CancleBtns.cancel, callback_data=EditCallbackBtn(type=callback_data))

          return self.as_markup()
     

class AdminKeyboardDelete(InlineKeyboardBuilder):
     
    def get_buttons(self, data: List[Tuple[int, str]], 
                    total_pages: int, page: int, callback_data: str): 
        

        for identity, title in data:
            self.button(text=title, callback_data=DeleteCallbackData(
                 type=EditBtnTxt.delete + callback_data.removeprefix(EditBtnTxt.type) + str(identity)))

        self.button(text="<-", callback_data=DeleteCallbackData(type=callback_data + str(page - 1))) if 1 < page else None
        self.button(text=CancleBtns.back, callback_data=EditCallbackData(type=callback_data))
        self.button(text="->", callback_data=DeleteCallbackData(type=callback_data + str(page + 1))) if page < total_pages else None

        self.adjust(*(*[1 for _ in data], 3))
        return self.as_markup()
    

class AdminKeyboardAddPostSelectCategory(InlineKeyboardBuilder):
     
    def get_buttons(self, data: List[Tuple[int, str]], 
                    total_pages: int, page: int, callback_data: str): 
        
        for identity, title in data:
            self.button(text=title, callback_data=AddCallbackData(
                 type=callback_data.removeprefix(EditBtnTxt.post) + str(identity)))

        self.button(text="<-", callback_data=AddCallbackData(type=callback_data + str(page - 1))) if 1 < page else None
        self.button(text=CancleBtns.back, callback_data=EditCallbackData(type=callback_data))
        self.button(text="->", callback_data=AddCallbackData(type=callback_data + str(page + 1))) if page < total_pages else None

        self.adjust(*(*[1 for _ in data], 3))
        return self.as_markup()
    
class AdminKeyboardDeleteSelectPost(InlineKeyboardBuilder):
     
    def get_buttons(self, data: List[Tuple[int, str]], category: str,
                    callback_data: str, page: int, total_pages: int): 
        
        for identity, title in data:
            self.button(text=title, callback_data=ConfirmDeletePost(type=category, identity=identity))

        self.button(text="<-", callback_data=DeleteCallbackData(type=callback_data + str(page - 1))) if 1 < page else None
        self.button(text=CancleBtns.back, callback_data=EditCallbackData(type=callback_data))
        self.button(text="->", callback_data=DeleteCallbackData(type=callback_data + str(page + 1))) if page < total_pages else None

        self.adjust(*(*[1 for _ in data], 3))
        return self.as_markup()