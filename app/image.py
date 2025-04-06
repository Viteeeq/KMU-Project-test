import numpy as np
import cv2
import json
import time
from database import PostamatDatabase


class ImageProcessing:
    def __init__(self):
        self.img_path = ''
        self.db = PostamatDatabase('postamat.db')
        self.db.create_table()
        self.name = 'randomname'
        # Загружаем предварительно обученный каскадный классификатор для определения лиц
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        # Загружаем предварительно обученную модель для распознавания лиц
        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    def faces_comparing(self, start_time):
        len_db = self.db.get_length()
        new_face = self.get_face_encoding(f"{self.name}.jpg")
        if new_face is None:
            print('Не удалось распознать лицо.')
            return 0, 0

        for i in range(1, len_db + 1):
            known_face, name, items = self.db.get_comparing_biometrics(i)
            try:
                if known_face is not None:
                    # Сравниваем лица с помощью OpenCV
                    result = self.compare_faces(known_face, new_face)
                    if result:
                        spend_time = time.time() - start_time
                        print(f'Это же {name}! Программа определила, что это вы за {spend_time}!')
                        return name, items
                    elif i == len_db:
                        print('Системе не удалось вас узнать, пожалуйста, сделайте новое фото!')
            except Exception as e:
                print(f'Ошибка при сравнении лиц: {str(e)}')
                return 0, 0

    def extract_face(self, username):
        try:
            # Загружаем изображение
            image = cv2.imread(f"{username}.jpg")
            if image is None:
                print("Не удалось загрузить изображение")
                return

            # Конвертируем в оттенки серого
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Определяем лица на изображении
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) == 0:
                print("Лицо не обнаружено на изображении")
                return

            # Берем первое обнаруженное лицо
            (x, y, w, h) = faces[0]
            face = gray[y:y+h, x:x+w]
            
            # Сохраняем лицо в базу данных
            face_data = json.dumps(face.tolist())
            self.db.add_user(input(), face_data, " 1: СНИЛС, 14: пропуск на работу, 22: Рюкзак, 4: Ключ от авто, 5: Головной убор")
            
        except Exception as e:
            print(f"Ошибка при обработке изображения: {str(e)}")
    
    def get_face_encoding(self, path):
        try:
            # Загружаем изображение
            image = cv2.imread(path)
            if image is None:
                print("Не удалось загрузить изображение")
                return None

            # Конвертируем в оттенки серого
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Определяем лица на изображении
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) == 0:
                print("Лицо не обнаружено на изображении")
                return None

            # Берем первое обнаруженное лицо
            (x, y, w, h) = faces[0]
            face = gray[y:y+h, x:x+w]
            
            return face
            
        except Exception as e:
            print(f"Ошибка при обработке изображения: {str(e)}")
            return None
            
    def compare_faces(self, known_face, new_face):
        try:
            # Приводим лица к одинаковому размеру
            known_face = cv2.resize(known_face, (100, 100))
            new_face = cv2.resize(new_face, (100, 100))
            
            # Вычисляем разницу между лицами
            diff = cv2.absdiff(known_face, new_face)
            mean_diff = np.mean(diff)
            
            # Если средняя разница меньше порога, считаем что это одно и то же лицо
            return mean_diff < 50
            
        except Exception as e:
            print(f"Ошибка при сравнении лиц: {str(e)}")
            return False