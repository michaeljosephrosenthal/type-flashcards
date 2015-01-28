import os, logging

DEV = os.environ.get("app_env", "Prod") == "Dev"
HOST = '0.0.0.0'
PORT = os.environ.get("PORT", 5000)
DATABASE_URL = os.environ.get("DATABASE_URL", "postgres://mjr:@localhost/type_flashcards")
INIT_DB = False
LOG_LEVEL = logging.DEBUG

logging.basicConfig(format='%(levelname)s: %(message)s', level=LOG_LEVEL)
logger = logging.getLogger()
l = logger
