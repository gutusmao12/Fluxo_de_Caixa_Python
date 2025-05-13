import psycopg2
import os

def get_db_connection():
    url = os.getenv("DATABASE_URL")
   
    # Render pode fornecer o URL com prefixo "postgres://", que precisa ser convertido
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://")
   
    return psycopg2.connect(url)