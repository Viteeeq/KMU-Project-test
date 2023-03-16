import sys
import cv2
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QPushButton


class VideoPlayer(QDialog):
    def __init__(self):
        super().__init__()

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())
