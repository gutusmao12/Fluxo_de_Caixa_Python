import psycopg2

def get_db_connection():
    return psycopg2.connect(
        host='localhost',
        user='postgres',
        password='DragoN12$%',
        database='caixa_fluxo',
        port=5433
    )