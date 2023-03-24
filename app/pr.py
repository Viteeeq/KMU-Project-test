import sys
import cv2
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

    def full_cycle(self, start_time):
        # self.extract_face(f'{self.name}.jpg', self.name)
        len_db = self.db.get_length()
        for i in range(1, len_db + 1):
            known_enc, name = self.db.get_comparing_biometrics(i)
            compare_res = self.discr_compare([known_enc], "randomname.jpg")[0]
            if compare_res:
                spend_time = time.time() - start_time
                print(f'Это же {name}! Программа определила, что это вы за {spend_time}!')
                break
            
    # def extract_face(self, username):
    #     known_photo = face_recognition.load_image_file(f"{username}.jpg") #
    #     try:
    #         known_encodings = np.array(face_recognition.face_encodings(known_photo)[0]).tolist()
    #         # self.db.add_user(input(), json.dumps(known_encodings), {1:'bebra'})
    #         return json.dumps(known_encodings)
    #         # print(face_recognition.face_encodings(known_photo)[0])
    #     except IndexError:
    #         print("Сделайте фото ещё раз, пожалуйста!")
            
    def discr_compare(self, known_enc, destination):
        try:
            image_to_compare = face_recognition.load_image_file(destination)  # загружаем фото которое надо сравнить
            image_to_compare_encoding = face_recognition.face_encodings(image_to_compare)[0]  # вычисляем дескриптор
            result = face_recognition.compare_faces(known_enc, image_to_compare_encoding, tolerance=0.5)  # получаем результат сравнения
            # print(result)
            return result
        except IndexError:
            print("Сфоткайся ещё раз, чзх.")