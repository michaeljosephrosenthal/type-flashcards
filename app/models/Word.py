from Core import Core, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

class Word(Core, Base):
    lang = Column(String, nullable=False)
    text = Column(String, nullable=False)
    category = Column(String, nullable=False)
    pronunciation = Column(String)

    translations = relationship(
        "Translation",
        primaryjoin="or_(Word.id==Translation.word_a_id, Word.id==Translation.word_b_id)")
    __table_args__ = (UniqueConstraint(lang, text, category),)
