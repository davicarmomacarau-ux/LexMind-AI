import sqlite3

DATABASE_NAME = "lexmind.db"

def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    # Tabela de Documentos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_arquivo TEXT NOT NULL,
            tipo_documento TEXT NOT NULL,
            conteudo_texto TEXT,
            status TEXT DEFAULT 'pendente',
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela de Analises/Validacoes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            documento_id INTEGER NOT NULL,
            resumo TEXT,
            conformidade_status TEXT,
            inconsistencias TEXT,
            FOREIGN KEY (documento_id) REFERENCES documentos (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def salvar_documento(nome_arquivo, tipo_documento, conteudo_texto):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO documentos (nome_arquivo, tipo_documento, conteudo_texto, status)
        VALUES (?, ?, ?, 'processado')
    ''', (nome_arquivo, tipo_documento, conteudo_texto))
    doc_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return doc_id

def salvar_analise(documento_id, resumo, conformidade_status, inconsistencias):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO analises (documento_id, resumo, conformidade_status, inconsistencias)
        VALUES (?, ?, ?, ?)
    ''', (documento_id, resumo, conformidade_status, inconsistencias))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Banco de dados LexMind-AI inicializado com sucesso.")