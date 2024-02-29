from aiogram.types.bot_command import BotCommand
from ..keyboards.Text.object import AdminEditBtnTxt

class Command:
    command: str
    description: str

    def __init__(self, command: str, description: str, admin: bool = False) -> None:
        self.command = command
        self.description = description
        self.no_prefix = command.removeprefix('/')
        self.admin = admin

    def __repr__(self) -> str:
        return str(f"{self.command}:{self.description}")

class CommandsBot:
    HOME = Command(command="/home", description=AdminEditBtnTxt.home)
    EDIT = Command(command="/edit", description=AdminEditBtnTxt.adminbtn, admin=True)
    EXESIZES = Command(command="/exesizes", description=AdminEditBtnTxt.exesizes)
    RECOMENDATIONS = Command(command="/recomandations", description=AdminEditBtnTxt.recomendations)
    TYPETRAININGS = Command(command="/trainigtype", description=AdminEditBtnTxt.typetrainigs)

    @staticmethod
    def get_bot_commands(admin: bool = False):
        if admin:
            return [BotCommand(command=i.command, description=i.description) for i in CommandsBot()]
        return [BotCommand(command=i.command, description=i.description) for i in CommandsBot() if i.admin is False]

    def __iter__(self):
        return iter([getattr(self, i) for i in self.__dir__() if isinstance(getattr(self, i), Command)])