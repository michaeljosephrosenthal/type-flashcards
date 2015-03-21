from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config 

from models import Base

engine = create_engine(config.DATABASE_URL, echo=False)
if config.INIT_DB:
    Base.metadata.create_all(engine)
    if config.KILL_AFTER_INIT_DB:
        exit(0)

create_session = sessionmaker(bind=engine)
