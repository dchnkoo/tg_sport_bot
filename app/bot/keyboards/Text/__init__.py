
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