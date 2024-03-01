

class StartButtonsTxt:
    home = "🏘️ На головну"
    exesizes = "🏋️‍♂️ Вправи"
    recomendations = "📝 Рекомендації"
    typetrainigs = "🎯 Види тренувань"

    @staticmethod
    def get_attr(attr: str):
        cls = StartButtonsTxt
        find = [getattr(cls, i) for i in vars(cls) if isinstance(getattr(cls, i), str) and attr.startswith(getattr(cls, i))]
        return find[0]
        

class AdminEditBtnTxt(StartButtonsTxt):
    adminbtn = "✏️ Редагувати"

class CancleBtns:
    back = "Назад"
    cancel = "Відміна"
    home = "На головну"

    skip = "Пропустити"
    go = "Далі"

class EditBtnTxt(CancleBtns):
    post = "Пост"
    type = "Категорію"

    add = "Додати"
    delete = "Видалити"

    confirm = "Підтвердити"
