import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    # Подключаемся к postgres для создания новой базы данных
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='13371337',
        host='localhost',
        port='5433'
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
    try:
        with conn.cursor() as cur:
            # Проверяем, существует ли база данных
            cur.execute("SELECT 1 FROM pg_database WHERE datname = 'biometric_db'")
            exists = cur.fetchone()
            
            if not exists:
                # Создаем базу данных
                cur.execute('CREATE DATABASE biometric_db')
                print("База данных biometric_db успешно создана")
            else:
                print("База данных biometric_db уже существует")
                
    except Exception as e:
        print(f"Ошибка при создании базы данных: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    create_database() 