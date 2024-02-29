from app.database.tables import (CategoryExesizes, RecomendationsType, TreningTypes,
                                 Recomendations, TreningViews, MediaExesizes)
from app.bot.keyboards.Text.object import StartButtonsTxt
from app.database.model.asyncc import async_db
from app.settings import logger
from sqlalchemy.exc import IntegrityError


async def get_correct_table(func, media: bool = False, only_table: bool = False, **kwargs) -> str:
    db = async_db()

    if (media and type) is (False or None):
        raise Exception("media and type must have another type")
    
    match (kwargs.get("type"), media):

        case (StartButtonsTxt.exesizes, False):
            if only_table: return CategoryExesizes
            return await func(db, CategoryExesizes, **kwargs)
        
        case (StartButtonsTxt.recomendations, False):
            if only_table: return RecomendationsType
            return await func(db, RecomendationsType, **kwargs)
        
        case (StartButtonsTxt.typetrainigs, False):
            if only_table: return TreningTypes
            return await func(db, TreningTypes, **kwargs)
        
        case (StartButtonsTxt.exesizes, True):
            if only_table: return MediaExesizes
            return await func(db, MediaExesizes, **kwargs)
        
        case (StartButtonsTxt.recomendations, True):
            if only_table: return Recomendations
            return await func(db, Recomendations, **kwargs)
        
        case (StartButtonsTxt.typetrainigs, True):
            if only_table: return TreningViews
            return await func(db, TreningViews, **kwargs)


async def insert_into_table(db: async_db, instance: object, **kwargs):
    category = kwargs.get("category")

    try: await db.async_insert_data(instance, to_dict=True, type=category)
    except IntegrityError as e:
        logger.error(f"Унікальна помилка:\n\nfunc: {insert_into_table.__name__}\ntable: {instance.__tablename__}\nError: {e}")
        return f"Категорія -> '{category}' вже присутня в системі"

    except Exception as e:
        logger.error(f"Помилка:\n\nfunc: {insert_into_table.__name__}\ntable: {instance.__tablename__}\nError: {e}")
        return f"Невідома помилка під час збереження категорії -> '{category}'"
    
    return f"Категорія -> {category} додана"