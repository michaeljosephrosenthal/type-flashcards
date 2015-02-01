from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config 

from models.models import Base, Word, Translation

engine = create_engine(config.DATABASE_URL, echo=False)
if config.INIT_DB: Base.metadata.create_all(engine)

create_session = sessionmaker(bind=engine)
