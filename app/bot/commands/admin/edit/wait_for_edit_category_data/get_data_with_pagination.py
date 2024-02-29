from app.database.model.asyncc import async_db
from app.settings import logger, DATA_PER_PAGE
        

async def get_category_with_pages(db: async_db, instance: object, **kwargs):
    page = kwargs.get("page")
    
    offset = (page - 1) * DATA_PER_PAGE

    try: data, total = await db.get_all_data(instance, True, offset=offset, limit=DATA_PER_PAGE)
    except Exception as e:
        logger.error(f"Помилка:\n\nfunc: {get_category_with_pages.__name__}\n\nError: {e}")
        return [[], 0]

    total_pages = (total + DATA_PER_PAGE - 1) // DATA_PER_PAGE

    return [[(i.id, i.type) for i in data], total_pages]