__all__ = ("Txt", "txtranslate")

from app.bot.language import TranslateString


class MainPage:
    HOME = "🏘️ На головну"
    EXESIZES = "🏋️‍♂️ Вправи"
    RECOMENDATIONS = "📝 Рекомендації"
    TYPETRAINYNGS = "🎯 Види тренувань"

class AdminText:
    EDIT = "✏️ Редагувати"

class CancelText:
    BACK = "Назад"
    CANCEL = "🚫"
    CANCEL_TXT = "Скасувати"

    SKIP = "Пропустити"
    GO = "Далі"

class EditTxt:
    POST = "Пост"
    TYPE = "Категорію"

    ADD = "Додати"
    DELETE = "Видалити"

    CONFIRM = "Підтвердити"

class Txt(
    MainPage,
    AdminText,
    CancelText,
    EditTxt
):
    ...

class TxtTranslate(
    Txt
):
    def __init__(self) -> None:
        for attr in self:
            setattr(self, attr, getattr(Txt, attr))
              
    def __getattribute__(self, __name: str):
        value = object.__getattribute__(self, __name)
        if isinstance(value, str):
            return TranslateString(value)
        return value
    
    def __iter__(self):
        return iter([i for i in self.__dir__() if i.isupper()])
    
txtranslate = TxtTranslate()