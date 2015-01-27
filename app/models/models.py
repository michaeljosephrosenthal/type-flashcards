from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Translation(Base):
    __tablename__ = 'translation'
    id = Column(Integer, primary_key=True)
    word_a_id = Column('word_a_id', Integer, ForeignKey('word.id'))
    word_b_id = Column('word_b_id', Integer, ForeignKey('word.id'))
    score = Column('score', Integer)

class Word(Base):
    __tablename__ = 'word'
    id = Column(Integer, primary_key=True)
    lang = Column(String)
    text = Column(String)
    def __repr__(self):
        return "<Word(lang='%s', text='%s')>" % (self.lang, self.text)
