import sqlite3

class PostamatDatabase:
    def __init__(self, db_file):
        self.db_file = db_file

    def create_table(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS postamat
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            biometrics TEXT NOT NULL,
                            items TEXT NOT NULL)''')

    def add_user(self, user_id, biometrics, items):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO postamat (user_id, biometrics, items)
                            VALUES (?, ?, ?)''', (user_id, str(biometrics), str(items)))

    def delete_user_by_id(self, id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''DELETE FROM postamat WHERE id = ?''', (id,))

    def delete_user_by_userid(self, user_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''DELETE FROM postamat WHERE user_id = ?''', (user_id,))

    def get_user(self, postamat_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM postamat WHERE id = ?''', (postamat_id,))
            row = cursor.fetchone()
            if row:
                postamat_id, user_id, biometrics, items = row
                return {'id': postamat_id, 'user_id': user_id, 'biometrics': biometrics,
                        'items': eval(items)}
            return "Данного пользователя нет в базе данных"

    def change_items(self, user_id, items):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''UPDATE postamat SET items = ? WHERE user_id = ?''',
                           (str(items), user_id))

if __name__ == "__main__":
    db = PostamatDatabase('postamat.db')
    db.create_table()


