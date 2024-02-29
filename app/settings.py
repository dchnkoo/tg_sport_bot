from pathlib import Path
import os


BASE_DIR = Path(__file__).parent.parent
ENV = os.environ

# SET DEBUG = False for no production enviroment
DEBUG = False

# postgres DB
DRIVER = "postgresql+asyncpg"
USER = "test"
PASSWORD = "test"
HOST = "localhost"
PORT = "5432"
DB = "test"

# ADMIN
ADMIN = int(ENV.get("ADMIN", "459557833"))

# BOT TOKEN
BOT_TOKEN = "6960403872:AAGYdk_8hHJ3nMppVGevZDA6lQbk9jsuKlA"


# logging
import logging

logger = logging
logger.basicConfig(filename=BASE_DIR / "app/app.log", filemode="w",
                             level=logging.INFO, format="'%(asctime)s - %(levelname)s: %(message)s'")


# ADMIN settings

DATA_PER_PAGE = 2