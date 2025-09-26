from sqlalchemy import Column, Integer, String
from database import Base

class Equipe(Base):
    __tablename__ = 'equipes_Tb'

    id_equipe = Column(Integer, primary_key=True)
    nome = Column(String(140))
    descricao = Column(String(140))

    def __repr__(self):
        return f"<Equipe(nome={self.nome}, descricao={self.descricao})>"

# Funções CRUD
