import psycopg2
import numpy as np
from typing import List, Tuple, Optional
import pickle

class BiometricDatabase:
    def __init__(self, dbname: str = 'biometric_db', user: str = 'postgres', 
                 password: str = '13371337', host: str = 'localhost', port: str = '5433'):
        """Инициализация подключения к базе данных"""
        self.conn_params = {
            'dbname': dbname,
            'user': user,
            'password': password,
            'host': host,
            'port': port
        }
        self._create_tables()

    def _create_tables(self) -> None:
        """Создание необходимых таблиц"""
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                # Создаем таблицу для хранения лиц
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS faces (
                        id SERIAL PRIMARY KEY,
                        user_id VARCHAR(50) NOT NULL,
                        face_data BYTEA NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()

    def add_face(self, user_id: str, face_data: np.ndarray) -> None:
        """Добавление нового лица в базу данных"""
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                # Сериализуем numpy массив в байты
                face_bytes = pickle.dumps(face_data)
                cur.execute(
                    "INSERT INTO faces (user_id, face_data) VALUES (%s, %s)",
                    (user_id, psycopg2.Binary(face_bytes))
                )
                conn.commit()

    def get_all_faces(self) -> List[Tuple[str, np.ndarray]]:
        """Получение всех лиц из базы данных"""
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT user_id, face_data FROM faces")
                results = []
                for user_id, face_data in cur.fetchall():
                    # Десериализуем байты обратно в numpy массив
                    face_array = pickle.loads(face_data)
                    results.append((user_id, face_array))
                return results

    def clear_database(self) -> None:
        """Очистка базы данных"""
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("TRUNCATE TABLE faces")
                conn.commit()

    def get_database_size(self) -> int:
        """Получение количества записей в базе данных"""
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM faces")
                return cur.fetchone()[0]

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    db = BiometricDatabase('postamat.db', 'user', 'password')
    db.create_tables()