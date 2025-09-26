def criar_tabela_tarefas():
    conn = sqlite3.connect('meubanco.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tarefas_Tb (
        id_tarefa INTEGER PRIMARY KEY,
        id_usuario INTEGER,
        titulo TEXT,
        descricao TEXT,
        data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
        data_conclusao DATETIME,
        status_id INTEGER,
        prioridade_id INTEGER,
        projeto_id INTEGER,
        FOREIGN KEY (id_usuario) REFERENCES usuarios_Tb(id_usuario),
        FOREIGN KEY (status_id) REFERENCES status_tarefas_Tb(id_status),
        FOREIGN KEY (prioridade_id) REFERENCES prioridades_Tb(id_prioridade),
        FOREIGN KEY (projeto_id) REFERENCES projetos_Tb(id_projeto)
    )
    ''')
    
    conn.commit()
    conn.close()

def inserir_tarefa(id_tarefa, id_usuario, titulo, descricao, data_conclusao=None):
    conn = sqlite3.connect('meubanco.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO tarefas_Tb (id_tarefa, id_usuario, titulo, descricao, data_conclusao)
    VALUES (?, ?, ?, ?, ?)
    ''', (id_tarefa, id_usuario, titulo, descricao, data_conclusao))
    
    conn.commit()
    conn.close()

# Exemplo de criação e inserção
criar_tabela_tarefas()
inserir_tarefa(1, 1, 'Desenvolver API', 'Desenvolver a API para o sistema', None)
