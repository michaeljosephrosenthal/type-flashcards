from util import uniqify, flatten
import sqlalchemy as a
from sqlalchemy import Integer, Numeric, String, TIMESTAMP
from sqlalchemy import ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.sql.functions import concat, current_timestamp, now
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship

Base = declarative_base()

class Default(object):
    id = a.Column(Integer, primary_key=True)
    created = a.Column(TIMESTAMP, server_default=now(), nullable=False)
    updated = a.Column(TIMESTAMP, server_default=now(), onupdate=current_timestamp(), nullable=False)

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
    word_a_id = a.Column('word_a_id', Integer, ForeignKey('word.id'))
    word_b_id = a.Column('word_b_id', Integer, ForeignKey('word.id'))
    score = a.Column('score', Numeric)
    __table_args__ = (CheckConstraint('word_a_id < word_b_id', name="ordered_ids"),
                      UniqueConstraint(word_a_id, word_b_id))
    def __init__(self, ida, idb, score=1):
        self.word_a_id, self.word_b_id = sorted({ida, idb})
        self.score = score

class Word(Default, Base):
    lang = a.Column(String, nullable=False)
    text = a.Column(String, nullable=False)
    category = a.Column(String, nullable=False)
    pronunciation = a.Column(String)
    __table_args__ = (UniqueConstraint(lang, text, category),)
