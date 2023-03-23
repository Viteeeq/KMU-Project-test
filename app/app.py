import sys
import cv2
import numpy as np
import face_recognition
import json
from PIL import Image
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QPushButton
from database import PostamatDatabase

class VideoPlayer(QDialog):
    def __init__(self):
        super().__init__()
        self.db = PostamatDatabase('postamat.db')
        self.db.create_table()

        # Создаем QLabel для отображения видео
        self.label = QLabel(self)
        self.label.setGeometry(100, 100, 680, 480)

        # Создаем таймер для получения новых кадров видео
        self.timer = QTimer(self)
        self.timer.setInterval(30)  # 30 миллисекунд между кадрами
        self.timer.timeout.connect(self.update_frame)
        self.setWindowTitle('Webcam')

        # Открываем видеопоток
        self.capture = cv2.VideoCapture(0)

        # Создаем кнопку для снимка
        self.snap_btn = QPushButton("Верификация", self)
        self.snap_btn.setGeometry(800, 100, 120, 50)
        self.snap_btn.clicked.connect(self.take_snapshot)
        # Запускаем таймер
        self.timer.start()

    def update_frame(self):
        # Считываем кадр из видеопотока
        ret, frame = self.capture.read()

        # Преобразуем кадр в QImage
        if ret:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h,
                              bytes_per_line, QImage.Format_RGB888)

            # Отображаем QImage в QLabel
            pixmap = QPixmap.fromImage(qt_image)
            self.label.setPixmap(pixmap)

    def take_snapshot(self):
        # Считываем текущий кадр из видеопотока
        ret, frame = self.capture.read()
        self.name = "randomname"

        # Сохраняем кадр в файл
        if ret:
            cv2.imwrite(f'{self.name}.jpg', frame)
        self.extract_face(f'{self.name}.jpg', self.name)
        # print(known_enc)
        len_db = self.db.get_length()
        for i in range(1, len_db + 1):
            known_enc = self.db.get_rekt(i)
            print(self.discr_compare([known_enc], "randomname.jpg"), ' ', i)
    
        # for i in range(1, len_db+1):
        #     print(self.discr_compare(json.loads(self.db.get_biometrics(i)), "randomname.jpg"), i)
        #     # print(self.db.get_biometrics(i), "randomname.jpg", i)
        
        
            
    def extract_face(self, photo_path, username):
        known_photo = face_recognition.load_image_file(f"{username}.jpg") #
        try:
            known_encodings = np.array(face_recognition.face_encodings(known_photo)[0]).tolist()
            smth = json.dumps(known_encodings)
            # print(face_recognition.face_encodings(known_photo)[0])
            # self.db.add_user(self.name, smth, {1:'bebra'})
            # print(self.db.get_user(1))
            # print(self.db.get_length())
        except IndexError:
            print("Сфоткайся ещё раз, чзх.")
        #   known_encodings = np.array(face_recognition.face_encodings(known_photo)[0]).tolist()
            
    def discr_compare(self, known_enc, destination):
        try:
            image_to_compare = face_recognition.load_image_file(destination)  # загружаем фото которое надо сравнить
            image_to_compare_encoding = face_recognition.face_encodings(image_to_compare)[0]  # вычисляем дескриптор
            result = face_recognition.compare_faces(known_enc, image_to_compare_encoding, tolerance=0.5)  # получаем результат сравнения
            # print(result)
            return result
        except IndexError:
            print("Сфоткайся ещё раз, чзх.")
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())
