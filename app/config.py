import os, logging
import dj_database_url
print dj_database_url

DEV = os.environ.get("app_env", "Prod") == "Dev"
HOST = '0.0.0.0'
PORT = os.environ.get("PORT", 5000)
DATABASE_URL = os.environ.get("DATABASE_URL")
LOG_LEVEL = logging.DEBUG

logging.basicConfig(format='%(levelname)s: %(message)s', level=LOG_LEVEL)
logger = logging.getLogger()
l = logger
