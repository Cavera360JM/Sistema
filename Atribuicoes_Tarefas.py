from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class AtribuicaoTarefa(Base):
    __tablename__ = 'atribuicoes_tarefas_Tb'

    id_tarefa = Column(Integer, ForeignKey('tarefas_Tb.id_tarefa'), primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuarios_Tb.id_usuario'), primary_key=True)
    data_atribuicao = Column(DateTime)
    papel = Column(String(255))

    tarefa = relationship("Tarefa", backref="atribuidos")
    usuario = relationship("Usuario", backref="atribuidos")

    def __repr__(self):
        return f"<AtribuicaoTarefa(papel={self.papel}, data_atribuicao={self.data_atribuicao})>"

# Funções CRUD
