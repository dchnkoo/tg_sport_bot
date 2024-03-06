from aiogram.types.bot_command import BotCommand
from app.bot.keyboards.Text import MainPage


class Commands:
    HOME = "home"
    EXESIZES = "exesizes"
    RECOMENDATIONS = "recomendations"
    TYPETRAINYNGS = "typetrainyngs"    
    edit = "edit"

    @staticmethod
    def get_command_type(command: str):
        for attr in Commands():
            if getattr(Commands, attr) == command:
                return getattr(MainPage, attr)

    def __iter__(self):
        return iter([i for i in self.__dir__() if i.isupper()])

class CommandsBot:
    
    def __init__(self) -> None:
        for attr in Commands():
            value = getattr(Commands, attr)
            setattr(self, attr.lower(), BotCommand(command="/" + value, description=getattr(MainPage, attr)))


    def __iter__(self):
        return iter([getattr(self, i) for i in self.__dir__() if isinstance(getattr(self, i), BotCommand)])