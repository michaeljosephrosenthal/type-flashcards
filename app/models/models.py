from app.util import uniqify, flatten
from sqlalchemy import Table, Column, Integer, Numeric, String, ForeignKey, UniqueConstraint, CheckConstraint, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import concat, current_timestamp, now

Base = declarative_base()

class Default(object):
    id = Column(Integer, primary_key=True)
    created = Column(TIMESTAMP, server_default=now(), nullable=False)
    updated = Column(TIMESTAMP, server_default=now(), onupdate=current_timestamp(), nullable=False)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __repr__(self):
        defining_columns = uniqify(flatten([[col.name for col in arg]
            for arg in self.__table_args__ if type(arg) == UniqueConstraint]))
        representation = "<" + self.__class__.__name__ + "(" + \
                    ", ".join([col + "='%s'" for col in defining_columns]) + ")>"
        return representation % tuple(map(self.__dict__.get, defining_columns))

class Translation(Default, Base):
    word_a_id = Column('word_a_id', Integer, ForeignKey('word.id'))
    word_b_id = Column('word_b_id', Integer, ForeignKey('word.id'))
    score = Column('score', Numeric)
    __table_args__ = (CheckConstraint('word_a_id < word_b_id', name="ordered_ids"),
                      UniqueConstraint(word_a_id, word_b_id))
    def __init__(self, ida, idb, score=1):
        self.word_a_id, self.word_b_id = sorted({ida, idb})
        self.score = score

class Word(Default, Base):
    lang = Column(String, nullable=False)
    text = Column(String, nullable=False)
    category = Column(String, nullable=False)
    pronunciation = Column(String)
    __table_args__ = (UniqueConstraint(lang, text, category),)
