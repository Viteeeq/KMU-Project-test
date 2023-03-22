from data_base.database import PostamatDatabase
import json

def check_bd():
    db = PostamatDatabase('postamat.db')
    db.create_table()
    db.add_user(123312, [51241, 241241, 412414, 1242141, 412421414, 4214214214352, 6456547], {'1': 1, '2': 2, '3': 3})
    print(db.get_user(1))
    db.change_items(user_id=123312, items={'1': 1, '2': 2, '3': 321, '4': 4})
    print(db.check_items(123312, '3'))
    print(db.get_items(user_id=123312))

if __name__ == "__main__":
    check_bd()

