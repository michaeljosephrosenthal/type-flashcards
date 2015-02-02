from sqlalchemy import Column, Integer, Numeric, String
from sqlalchemy import ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from Core import Core, Base

class Translation(Core, Base):
    extend_existing=True
    word_a_id = Column(Integer, ForeignKey('word.id'), nullable=False)
    word_b_id = Column(Integer, ForeignKey('word.id'), nullable=False)
    score = Column('score', Numeric)
    word_a = relationship("Word", foreign_keys=[word_a_id])
    word_b = relationship("Word", foreign_keys=[word_b_id])
    __table_args__ = (CheckConstraint('word_a_id < word_b_id', name="ordered_ids"),
                      UniqueConstraint(word_a_id, word_b_id))
    def __init__(self, ida, idb, score=1):
        self.word_a_id, self.word_b_id = sorted({ida, idb})
        self.score = score
    def materialize(self):
        return {self.word_a.lang: self.word_a.text,
                self.word_b.lang: self.word_b.text}
