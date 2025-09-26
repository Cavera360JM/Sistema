def criar_tabela_subtarefas():
    conn = sqlite3.connect('meubanco.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS subtarefas_Tb (
        id_subtarefa INTEGER PRIMARY KEY,
        id_tarefa_pai INTEGER,
        titulo TEXT,
        status_id INTEGER,
        data_conclusao DATETIME,
        FOREIGN KEY (id_tarefa_pai) REFERENCES tarefas_Tb(id_tarefa),
        FOREIGN KEY (status_id) REFERENCES status_tarefas_Tb(id_status)
    )
    ''')
    
    conn.commit()
    conn.close()

def inserir_subtarefa(id_subtarefa, id_tarefa_pai, titulo, status_id, data_conclusao=None):
    conn = sqlite3.connect('meubanco.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO subtarefas_Tb (id_subtarefa, id_tarefa_pai, titulo, status_id, data_conclusao)
    VALUES (?, ?, ?, ?, ?)
    ''', (id_subtarefa, id_tarefa_pai, titulo, status_id, data_conclusao))
    
    conn.commit()
    conn.close()

# Exemplo de criação e inserção
criar_tabela_subtarefas()
inserir_subtarefa(1, 1, 'Subtarefa: Desenvolvimento de Módulo', 1, None)
