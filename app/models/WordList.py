from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from Core import Core, Base

class WordListItem(Core, Base):
    wordlist_id = Column(Integer, ForeignKey('wordlist.id'))
    translation_id = Column(Integer, ForeignKey('translation.id'))
    translation = relationship("Translation", foreign_keys=[translation_id])
    __table_args__ = (UniqueConstraint(wordlist_id, translation_id),)
    def materialize(self):
        return self.translation.materialize()

class WordList(Core, Base):
    name = Column(String, nullable=False)
    items = relationship("WordListItem", backref="wordlist")
    __table_args__ = (UniqueConstraint(name),)
    def __init__(self, name, translations, session):
        self.name = name 
        self.persist(session)
        session.add_all([WordListItem(wordlist_id = self.id, translation_id = t.id)
            for t in translations])
        session.commit()
    def materialize(self):
        return {"name": self.name,
                "items": [i.materialize() for i in self.items]}
