def criar_tabela_status_tarefas():
    conn = sqlite3.connect('meubanco.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS status_tarefas_Tb (
        id_status INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        descricao TEXT NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()

def inserir_status_tarefa(id_status, nome, descricao):
    conn = sqlite3.connect('meubanco.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO status_tarefas_Tb (id_status, nome, descricao)
    VALUES (?, ?, ?)
    ''', (id_status, nome, descricao))
    
    conn.commit()
    conn.close()

# Exemplo de criação e inserção
criar_tabela_status_tarefas()
inserir_status_tarefa(1, 'Em Progresso', 'Tarefa está em andamento.')
