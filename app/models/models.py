from sqlalchemy import Table, Column, Integer, Numeric, String, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
class Translation(Base):
    __tablename__ = 'translation'
    id = Column(Integer, primary_key=True)
    word_a_id = Column('word_a_id', Integer, ForeignKey('word.id'))
    word_b_id = Column('word_b_id', Integer, ForeignKey('word.id'))
    score = Column('score', Numeric)

class Word(Base):
    __tablename__ = 'word'
    id = Column(Integer, primary_key=True)
    lang = Column(String)
    text = Column(String)
    pronunciation = Column(String)
    category = Column(String)
    __table_args__ = (UniqueConstraint('lang', 'text', 'category'),)
    def __repr__(self):
        return "<Word(lang='%s', text='%s')>" % (self.lang, self.text)
