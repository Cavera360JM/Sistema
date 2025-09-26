def criar_tabela_projetos():
    conn = sqlite3.connect('meubanco.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS projetos_Tb (
        id_projeto INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        descricao TEXT,
        data_inicio DATE,
        data_fim DATE,
        id_usuario_responsavel INTEGER,
        FOREIGN KEY (id_usuario_responsavel) REFERENCES usuarios_Tb(id_usuario)
    )
    ''')
    
    conn.commit()
    conn.close()

def inserir_projeto(id_projeto, nome, descricao, data_inicio, data_fim, id_usuario_responsavel):
    conn = sqlite3.connect('meubanco.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO projetos_Tb (id_projeto, nome, descricao, data_inicio, data_fim, id_usuario_responsavel)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (id_projeto, nome, descricao, data_inicio, data_fim, id_usuario_responsavel))
    
    conn.commit()
    conn.close()

# Exemplo de criação e inserção
criar_tabela_projetos()
inserir_projeto(1, 'Sistema de Gerenciamento', 'Projeto de desenvolvimento de um sistema', '2025-01-01', '2025-12-31', 1)
