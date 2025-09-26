import sqlite3

def criar_tabela_usuarios():
    conn = sqlite3.connect('meubanco.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios_Tb (
        id_usuario INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        email TEXT NOT NULL,
        senha_hash TEXT NOT NULL,
        data_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
        status_conta BLOB
    )
    ''')
    
    conn.commit()
    conn.close()

def inserir_usuario(id_usuario, nome, email, senha_hash, status_conta=None):
    conn = sqlite3.connect('meubanco.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO usuarios_Tb (id_usuario, nome, email, senha_hash, status_conta)
    VALUES (?, ?, ?, ?, ?)
    ''', (id_usuario, nome, email, senha_hash, status_conta))
    
    conn.commit()
    conn.close()

# Exemplo de criação e inserção
criar_tabela_usuarios()
inserir_usuario(1, 'João Silva', 'joao@example.com', 'hash123', None)
