from sqlalchemy import Column, Integer, String
from database import Base

class Tag(Base):
    __tablename__ = 'tags_Tb'

    id_tag = Column(Integer, primary_key=True)
    nome = Column(String(255))

    def __repr__(self):
        return f"<Tag(nome={self.nome})>"

# Funções CRUD
