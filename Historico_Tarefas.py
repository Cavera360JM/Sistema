from sqlalchemy import Column, Integer, String, ForeignKey, Binary
from sqlalchemy.orm import relationship
from database import Base

class HistoricoTarefa(Base):
    __tablename__ = 'historico_tarefas_Tb'

    id_historico = Column(Integer, primary_key=True)
    id_tarefa = Column(Integer, ForeignKey('tarefas_Tb.id_tarefa'))
    id_usuario = Column(Integer, ForeignKey('usuarios_Tb.id_usuario'))
    tipo_alteracao = Column(Binary)

    tarefa = relationship("Tarefa", backref="historico")
    usuario = relationship("Usuario", backref="historico")

    def __repr__(self):
        return f"<HistoricoTarefa(tipo_alteracao={self.tipo_alteracao})>"

# Funções CRUD
