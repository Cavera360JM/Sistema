def criar_tabela_prioridades():
    conn = sqlite3.connect('meubanco.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS prioridades_Tb (
        id_prioridade INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        nivel TEXT CHECK(nivel IN ('Baixo', 'Médio', 'Alto'))
    )
    ''')
    
    conn.commit()
    conn.close()

def inserir_prioridade(id_prioridade, nome, nivel):
    conn = sqlite3.connect('meubanco.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO prioridades_Tb (id_prioridade, nome, nivel)
    VALUES (?, ?, ?)
    ''', (id_prioridade, nome, nivel))
    
    conn.commit()
    conn.close()

# Exemplo de criação e inserção
criar_tabela_prioridades()
inserir_prioridade(1, 'Urgente', 'Alto')
