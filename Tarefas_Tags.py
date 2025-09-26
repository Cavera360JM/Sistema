from sqlalchemy import Column, Integer, ForeignKey
from database import Base

class TarefaTag(Base):
    __tablename__ = 'tarefas_tags_Tb'

    id_tarefa = Column(Integer, ForeignKey('tarefas_Tb.id_tarefa'), primary_key=True)
    id_tag = Column(Integer, ForeignKey('tags_Tb.id_tag'), primary_key=True)

    def __repr__(self):
        return f"<TarefaTag(id_tarefa={self.id_tarefa}, id_tag={self.id_tag})>"

# Funções CRUD
