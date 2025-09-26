from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class MembroEquipe(Base):
    __tablename__ = 'membros_equipes_Tb'

    id_usuario = Column(Integer, ForeignKey('usuarios_Tb.id_usuario'), primary_key=True)
    id_equipe = Column(Integer, ForeignKey('equipes_Tb.id_equipe'), primary_key=True)
    cargo = Column(String(255))
    data_entrada = Column(DateTime)

    usuario = relationship("Usuario", backref="membros_equipe")
    equipe = relationship("Equipe", backref="membros")

    def __repr__(self):
        return f"<MembroEquipe(cargo={self.cargo}, data_entrada={self.data_entrada})>"

# Funções CRUD
