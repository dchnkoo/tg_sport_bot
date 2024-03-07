from aiogram.filters.callback_data import CallbackData


# DELETE CALLBACK MESSAGE
class DeleteCallbackMsg(CallbackData, prefix="DELCBMSG"):
    delete: bool = True 


# ADMIN
class SelectEditType(CallbackData, prefix="SEL"):
    type: str
    lang: str = "uk"



    # category
class EditCategory(CallbackData, prefix="EDC"):
    type: str
    lang: str = "uk"


class AddCategory(CallbackData, prefix="ADDC"):
    type: str
    lang: str = "uk"


class DeleteCategory(CallbackData, prefix="DELC"):
    type: str
    page: int = 1
    lang: str = "uk"


    # post
class EditPost(CallbackData, prefix="EDP"):
    type: str
    lang: str = "uk"


class SelectCategoryForPostAdd(CallbackData, prefix="SCFPA"):
    type: str
    page: int = 1
    lang: str = "uk"


class SelectCategoryForPostDelete(CallbackData, prefix="SCFPD"):
    type: str
    page: int = 1 
    lang: str = "uk"


class AddPost(CallbackData, prefix="ADDP"):
    type: str
    identity: int
    lang: str = "uk"


class DeletePost(CallbackData, prefix="DELP"):
    type: str
    category: int
    identity: int
    lang: str = "uk"


class SelectPostToDelete(CallbackData, prefix="SPTD"):
    type: str
    identity: int
    page: int = 1
    lang: str = "uk"




class Delete(CallbackData, prefix="DEL"):
    type: str
    identity: int
    lang: str = "uk"


# USER
    
class PostFromCategorySelect(CallbackData, prefix="PFCS"):
    type: str
    identity: int
    page: int = 1
    lang: str = "uk"


class UserChooseCategory(CallbackData, prefix="UCC"):
    type: str
    page: int = 1
    lang: str = "uk"

class GetUserPost(CallbackData, prefix="GUP"):
    type: str
    category: int
    identity: int
    lang: str = "uk"
