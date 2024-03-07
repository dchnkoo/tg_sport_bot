from pathlib import Path
import os, json


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
ADMIN = json.loads(ENV.get("ADMIN", '[]'))

# BOT TOKEN
BOT_TOKEN = ""


# logging
import logging

logger = logging
logger.basicConfig(filename=BASE_DIR / "app/app.log", filemode="w",
                             level=logging.INFO, format="'%(asctime)s - %(levelname)s: %(message)s'")


# ADMIN settings

DATA_PER_PAGE = 4

MEDIA_LIMIT = 9

VIDEO_LIMIT = 20
PHOTO_LIMMIT = 5

BUTTONS_LIMIT = 3