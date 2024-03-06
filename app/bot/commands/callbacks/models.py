from aiogram.filters.callback_data import CallbackData


# DELETE CALLBACK MESSAGE
class DeleteCallbackMsg(CallbackData, prefix="DELCBMSG"):
    delete: bool = True 


# ADMIN
class SelectEditType(CallbackData, prefix="SEL"):
    type: str



    # category
class EditCategory(CallbackData, prefix="EDC"):
    type: str

class AddCategory(CallbackData, prefix="ADDC"):
    type: str

class DeleteCategory(CallbackData, prefix="DELC"):
    type: str
    page: int = 1



    # post
class EditPost(CallbackData, prefix="EDP"):
    type: str

class SelectCategoryForPostAdd(CallbackData, prefix="SCFPA"):
    type: str
    page: int = 1

class SelectCategoryForPostDelete(CallbackData, prefix="SCFPD"):
    type: str
    page: int = 1 

class AddPost(CallbackData, prefix="ADDP"):
    type: str
    identity: int

class DeletePost(CallbackData, prefix="DELP"):
    type: str
    category: int
    identity: int

class SelectPostToDelete(CallbackData, prefix="SPTD"):
    type: str
    identity: int
    page: int = 1




class Delete(CallbackData, prefix="DEL"):
    type: str
    identity: int


# USER
    
class PostFromCategorySelect(CallbackData, prefix="PFCS"):
    type: str
    identity: int
    page: int = 1


class UserChooseCategory(CallbackData, prefix="UCC"):
    type: str
    page: int = 1

class GetUserPost(CallbackData, prefix="GUP"):
    type: str
    category: int
    identity: int