from app.database.model.asyncc import async_db
from app.settings import logger, DATA_PER_PAGE
from sqlalchemy.exc import IntegrityError
from app.database.tables import *
from ..keyboards.Text import Txt
from typing import Tuple


class ModelDataManipulation(async_db):

    def __init__(self, type: str, media: bool = False) -> None:
        super().__init__()
        self.__type = type
        self.__media = media
        self.table = self.get_table()

    
    async def insert_data(self, **kwargs):
        try: await self.async_insert_data(self.table, get_data=False, **kwargs) 
        except IntegrityError as e:
            logger.error(e)
            return False, "Ви намагаєтесь додати дані які мають бути унікальними.\nПомилка виникає через те що такі данні вже присутні в системі."

        except Exception as e:
            logger.error(e)
            return False, "Невідома помилка. Спробуйте ще раз"

        return True, f"Данні для > {self.__type} < були додані успішно!"

    async def delete_data(self, and__ = None, exp = None):
        try: await self.async_delete_data(self.table, and__=and__, exp=exp)
        except Exception as e:
            logger.error(e)
            return False, "Невідома помилка. Спробуйте ще раз"
        
        return True, f"Данні були видаленні в -> {self.__type}"
    
    async def get_data_pagination(
            
            self, 
            and__: None = None,
            exp: None = None,
            get_all: bool = True,
            page: int = 1

        ) -> Tuple[Tuple[int, str], int]:

        offset = (page - 1) * DATA_PER_PAGE

        some_data = {"count": True, "offset": offset, "limit": DATA_PER_PAGE}
        try: 
            if get_all:
                data, total = await self.get_all_data(self.table, **some_data)
            else:
                data, total = await self.async_get_where(self.table, and__=and__, exp=exp, **some_data)
        except Exception as e:
            logger.error(e)
            return [[], 0]
        
        total_pages = (total + DATA_PER_PAGE - 1) // DATA_PER_PAGE

        return [[(i.id, i.title if self.__media else i.type) for i in data], total_pages]


    def get_table(self):
        match (self.__type, self.__media):

            case (Txt.EXESIZES, False):
                return CategoryExesizes
            
            case (Txt.RECOMENDATIONS, False):
                return RecomendationsType
            
            case (Txt.TYPETRAINYNGS, False):
                return TreningTypes
            
            case (Txt.EXESIZES, True):
                return MediaExesizes
            
            case (Txt.RECOMENDATIONS, True):
                return Recomendations
            
            case (Txt.TYPETRAINYNGS, True):
                return TreningViews
