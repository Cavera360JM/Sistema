def criar_tabela_comentarios():
    conn = sqlite3.connect('meubanco.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS comentarios_Tb (
        id_comentario INTEGER PRIMARY KEY,
        id_tarefa INTEGER,
        id_usuario INTEGER,
        conteudo TEXT,
        data_comentario DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_tarefa) REFERENCES tarefas_Tb(id_tarefa),
        FOREIGN KEY (id_usuario) REFERENCES usuarios_Tb(id_usuario)
    )
    ''')
    
    conn.commit()
    conn.close()

def inserir_comentario(id_comentario, id_tarefa, id_usuario, conteudo):
    conn = sqlite3.connect('meubanco.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO comentarios_Tb (id_comentario, id_tarefa, id_usuario, conteudo)
    VALUES (?, ?, ?, ?)
    ''', (id_comentario, id_tarefa, id_usuario, conteudo))
    
    conn.commit()
    conn.close()

# Exemplo de criação e inserção
criar_tabela_comentarios()
inserir_comentario(1, 101, 1, 'Este é um comentário sobre a tarefa.')
