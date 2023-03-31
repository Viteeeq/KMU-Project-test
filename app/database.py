import sqlite3
import json

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

    def get_user(self, id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM postamat WHERE id = ?''', (id,))
            row = cursor.fetchone()
            if row:
                id, user_id, biometrics, items = row
                return {'id': id, 'user_id': user_id, 'biometrics': eval(biometrics),
                        'items': eval(items)}
            return "Данного пользователя нет в базе данных"
        
    # def get_biometrics(self, id):
    #     with sqlite3.connect(self.db_file) as conn:
    #         cursor = conn.cursor()
    #         cursor.execute('''SELECT * FROM postamat WHERE id = ?''', (id,))
    #         row = cursor.fetchone()
    #         if row:
    #             _, _, biometrics, _ = row
    #             return eval(biometrics)
    #         return "Данного пользователя нет в базе данных"

    def change_items(self, user_id, items):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''UPDATE postamat SET items = ? WHERE user_id = ?''',
                           (str(items), user_id))

    def check_items(self, user_id, item_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM postamat WHERE user_id = ?''', (user_id,))
            row = cursor.fetchone() 
            if row:
                _, _, _, items = row
                return eval(items)[item_id]
            return "Данного предмета нет в базе данных"

    def get_items(self, user_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM postamat WHERE user_id = ?''', (user_id,))
            row = cursor.fetchone() 
            if row:
                _, _, _, items = row
                return items
            return "Данного предмета нет в базе данных"
    
    def get_length(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM postamat''')
            row = cursor.fetchall()
            return len(row)
        
    def get_comparing_biometrics(self, id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM postamat WHERE id = ?''', (id,))
            row = cursor.fetchone()
            items = row[3]
            temp = json.loads(row[2])
            username = row[1]
            return temp, username, items


if __name__ == "__main__":
    db = PostamatDatabase('postamat.db')
    db.create_table()