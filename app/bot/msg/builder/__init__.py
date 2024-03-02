from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List, Tuple
from aiogram import types 
import base64


class BuildTelegramMsg:

    def __init__(self, title: str, media: List[Tuple[str, bytes]], 
                 text: str, buttons: List[List[Tuple[str, str]]], type: str) -> None:
        self._title = title
        self._media = media
        self._text = text
        self._buttons = buttons
        self._type = type

    
    def __get_title(self) -> str:
       return f"{self._type}: {self._title}"

    
    def __get_text(self) -> str:
        return self.__get_title() + "\n\n" + self._text
    

    def get_media_group(self, decode: bool = False) -> List[types.InputMediaVideo | types.InputMediaPhoto]:
        return [
        types.InputMediaVideo(
            media=types.BufferedInputFile(base64.b64decode(value) if decode else value, filename="some.mp4")
        ) if content == "VIDEO" else types.InputMediaPhoto(
            media=types.BufferedInputFile(base64.b64decode(value) if decode else value, filename="some.jpg")
        )
          for content, value in self._media
        ]
        
    def __get_buttons(self) -> types.InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()

        [keyboard.button(**dict((txt, url))) for txt, url in self._buttons]

        keyboard.adjust(1)

        return keyboard.as_markup()

    def get_msg(self):
        return {
            "text": self.__get_text(),
            "reply_markup": self.__get_buttons()
        }