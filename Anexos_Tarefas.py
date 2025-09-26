from sqlalchemy import Column, Integer, ForeignKey
from database import Base

class AnexoTarefa(Base):
    __tablename__ = 'anexos_tarefas_Tb'

    id_anexo = Column(Integer, primary_key=True)
    id_tarefa = Column(Integer, ForeignKey('tarefas_Tb.id_tarefa'))
    id_arquivo = Column(Integer, ForeignKey('arquivos_Tb.id_arquivo'))

    def __repr__(self):
        return f"<AnexoTarefa(id_tarefa={self.id_tarefa}, id_arquivo={self.id_arquivo})>"

# Funções CRUD
