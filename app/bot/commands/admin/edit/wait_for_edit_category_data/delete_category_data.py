from app.database.model.asyncc import async_db
from app.settings import logger


async def delete_from_db_by_id(db: async_db, instance: object, **kwargs):
    identity = kwargs.get("identity")

    try: await db.async_delete_data(instance, exp=instance.id == identity)
    except Exception as e:
        logger.error(f"Помилка\n\nfunc: {delete_from_db_by_id.__name__}\nError: {e}")
        return "Сталась помилка під час видалення"
    
    return "Видаленно"