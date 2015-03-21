import os, logging

DEV = os.environ.get("app_env", "Prod") == "Dev"
HOST = os.environ.get("host", '0.0.0.0')
PORT = os.environ.get("PORT", 8000)
DATABASE_URL = os.environ.get("DATABASE_URL", "postgres://mjr:@localhost/type_flashcards")
INIT_DB = os.environ.get("INIT_DB", False)
KILL_AFTER_INIT_DB = os.environ.get("KILL_AFTER_INIT_DB", False)
LOG_LEVEL = logging.DEBUG

logging.basicConfig(format='%(levelname)s: %(message)s', level=LOG_LEVEL)
logger = logging.getLogger()
l = logger
