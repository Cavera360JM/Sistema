def criar_tabela_anexos_tarefas():
    conn = sqlite3.connect('meubanco.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS anexos_tarefas_Tb (
        id_anexo INTEGER PRIMARY KEY,
        id_tarefa INTEGER,
        id_arquivo INTEGER,
        FOREIGN KEY (id_tarefa) REFERENCES tarefas_Tb(id_tarefa),
        FOREIGN KEY (id_arquivo) REFERENCES arquivos_Tb(id_arquivo)
    )
    ''')
    
    conn.commit()
    conn.close()

def inserir_anexo_tarefa(id_anexo, id_tarefa, id_arquivo):
    conn = sqlite3.connect('meubanco.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO anexos_tarefas_Tb (id_anexo, id_tarefa, id_arquivo)
    VALUES (?, ?, ?)
    ''', (id_anexo, id_tarefa, id_arquivo))
    
    conn.commit()
    conn.close()

# Exemplo de criação e inserção
criar_tabela_anexos_tarefas()
inserir_anexo_tarefa(1, 1, 1)
