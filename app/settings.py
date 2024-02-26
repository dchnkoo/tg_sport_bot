from pathlib import Path


BASE_DIR = Path(__file__).parent.parent

# SET DEBUG = False for no production enviroment
DEBUG = True

# postgres DB
DRIVER = "postgresql+asyncpg"
USER = "test"
PASSWORD = "test"
HOST = "localhost"
DB = "test"