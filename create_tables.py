# create_tables.py
import psycopg2
import os

def create_tables():
    url = os.getenv("DATABASE_URL")
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://")
   
    conn = psycopg2.connect(url)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entradas (
            id SERIAL PRIMARY KEY,
            descricao TEXT NOT NULL,
            valor NUMERIC NOT NULL,
            data DATE NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saidas (
            id SERIAL PRIMARY KEY,
            descricao TEXT NOT NULL,
            valor NUMERIC NOT NULL,
            data DATE NOT NULL
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("Tabelas criadas com sucesso.")

if __name__ == "__main__":
    create_tables()