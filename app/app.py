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

        # Сохраняем кадр в файл
        if ret:
            cv2.imwrite('snapshot.jpg', frame)
        self.name = "randomname"
        self.extract_face("snapshot.jpg", self.name)
        
            
    def extract_face(self, photo_path, username):
        faces = face_recognition.load_image_file(photo_path) #
        faces_locations = face_recognition.face_locations(faces)

        for face_location in faces_locations:
            top, right, bottom, left = face_location

            face_img = faces[top:bottom, left:right]
            pil_img = Image.fromarray(face_img)
            pil_img.save(f"{username}.jpg") #
        known_photo = face_recognition.load_image_file(f"{username}.jpg") #
        try:
            known_encodings = np.array(face_recognition.face_encodings(known_photo)[0]).tolist()
            self.db.add_user(self.name, known_encodings, {})
            print(self.db.get_user(1))
            # return json.dumps()
        except IndexError:
            print("Сфоткайся ещё раз, чзх.")
        #   known_encodings = np.array(face_recognition.face_encodings(known_photo)[0]).tolist()
            
    def discr_compare(self, known_enc, destination):
        image_to_compare = face_recognition.load_image_file(destination)  # загружаем фото которое надо сравнить
        image_to_compare_encoding = face_recognition.face_encodings(image_to_compare)[0]  # вычисляем дескриптор
        result = face_recognition.compare_faces([known_enc], image_to_compare_encoding, tolerance=0.5)  # получаем результат сравнения
        return result
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())
