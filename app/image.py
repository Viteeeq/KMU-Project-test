import numpy as np
import face_recognition
import json
import time
from database import PostamatDatabase


class ImageProcessing:
    def __init__(self):
        self.img_path = ''
        self.db = PostamatDatabase('postamat.db')
        self.db.create_table()

    def faces_comparing(self, start_time):
        len_db = self.db.get_length()
        new_enc = self.get_face_encodings("randomname.jpg")
        for i in range(1, len_db + 1):
            known_enc, name, items = self.db.get_comparing_biometrics(i)
            try:
                compare_res = self.discr_compare([known_enc], new_enc)[0]
                if compare_res:
                    spend_time = time.time() - start_time
                    print(f'Это же {name}! Программа определила, что это вы за {spend_time}!')
                    break
            except TypeError:
                print('Пожалуйста, сделайте новое фото!')
                break
        # self.extract_face('randomname')
                     
    def extract_face(self, username): # использовать только для добавления нового пользователя напрямую! можно использовать для инициализации!
        known_photo = face_recognition.load_image_file(f"{username}.jpg") #
        try:
            known_encodings = np.array(face_recognition.face_encodings(known_photo)[0]).tolist()
            smth = json.dumps(known_encodings)
            self.db.add_user(input(), smth, {15:'bebra', 16:'seledka'}) #здесь можно вручную ввести данные для добавления.
        except IndexError:
            print("Сфоткайся ещё раз, чзх.")
    
    def get_face_encodings(self, path):
        try:
            image_to_compare = face_recognition.load_image_file(path)  # загружаем фото которое надо сравнить
            image_to_compare_encoding = face_recognition.face_encodings(image_to_compare)[0]  # вычисляем дескриптор
            return image_to_compare_encoding
        except IndexError:
            print('Не удалось распознать лицо.', end = ' ')
            
    def discr_compare(self, known_enc, new_encoding):
        result = face_recognition.compare_faces(known_enc, new_encoding, tolerance=0.5)  # получаем результат сравнения
        return result