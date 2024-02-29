from app.settings import DRIVER, USER, PASSWORD, HOST, PORT, DB

from sqlalchemy.ext.asyncio import create_async_engine
import os


env = os.environ

DRIVER = env.get("DB_DRIVER", DRIVER)
USER = env.get("POSTGRES_USER", USER)
PASSWORD = env.get("POSTGRES_PASSWORD", PASSWORD)
HOST = env.get("DB_HOST", HOST)
PORT = env.get("DB_PORT", PORT)
DB = env.get("POSTGRES_DB", DB)

url = f"{DRIVER}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"

engine = create_async_engine(url)