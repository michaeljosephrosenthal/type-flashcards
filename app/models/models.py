from util import uniqify, flatten
from sqlalchemy import Column, Integer, Numeric, String, TIMESTAMP
from sqlalchemy import ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.sql.functions import concat, current_timestamp, now
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship

Base = declarative_base()

class Default(object):

    id = Column(Integer, primary_key=True)
    created = Column(TIMESTAMP, server_default=now(), nullable=False)
    updated = Column(TIMESTAMP, server_default=now(), onupdate=current_timestamp(), nullable=False)

    @property
    def __identifier_keys__(self):
        return uniqify(flatten(
            [[col.name for col in arg]
                for arg in self.__table_args__ if type(arg) == UniqueConstraint]))

    @property
    def __identifiers__(self):
        return { k: getattr(self, k) for k in self.__identifier_keys__}

    @property
    def __unique_filters__(self):
        """Maps the sqlalchemy base classes to the object's cooresponding attributes with ==, returning a list of binary expressions"""
        return map(lambda x,y: x==y,
                [getattr(self.__class__, c) for c in self.__identifiers__],
                [getattr(self, a) for a in self.__identifiers__])

    def sync_with(self, session):
        self.id = session.query(getattr(self.__class__, "id")).\
                filter(*self.__unique_filters__).scalar()
        if self.id: session.merge(self)
        else: session.add(self)
        return self

    def persist(self, session):
        """Checks for the existence of an object in a session based on unique constraints, adding the id to the app object if it does exist and inserting the app object into the database  otherwise"""
        self.sync_with(session)
        session.commit()

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __repr__(self):
        defining_columns = self.__identifier_keys__
        representation = "<" + self.__class__.__name__ + "(" + \
                    ", ".join([col + "='%s'" for col in defining_columns]) + ")>"
        return representation % tuple(map(lambda a: getattr(self, a), defining_columns))

class Translation(Default, Base):
    word_a_id = Column(Integer, ForeignKey('word.id'))
    word_b_id = Column(Integer, ForeignKey('word.id'))
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

class WordListItem(Default, Base):
    wordlist_id = Column(Integer, ForeignKey('wordlist.id'))
    translation_id = Column(Integer, ForeignKey('translation.id'))
    __table_args__ = (UniqueConstraint(wordlist_id, translation_id),)

class WordList(Default, Base):
    name = Column(String, nullable=False)
    __table_args__ = (UniqueConstraint(name),)
    def __init__(self, name, translations, session):
        self.name = name 
        self.persist(session)
        session.add_all([WordListItem(wordlist_id = self.id, translation_id = t.id)
            for t in translations])
        session.commit()
