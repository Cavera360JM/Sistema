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
    
    conn.c
