import sys
import cv2
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QLabel


class VideoPlayer(QDialog):
    def __init__(self):
        super().__init__()

        # Создаем QLabel для отображения видео
        self.label = QLabel(self)
        self.label.resize(640, 480)
        self.setWindowTitle('Webcam')

        # Создаем таймер для получения новых кадров видео
        self.timer = QTimer(self)
        self.timer.setInterval(30)  # 30 миллисекунд между кадрами
        self.timer.timeout.connect(self.update_frame)

        # Открываем видеопоток
        self.capture = cv2.VideoCapture(0)
        

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
            # cur_time = round(time.time() - start_time, 2)
            # photo_counter = int(cur_time // 0.5)
            # print(photo_counter)
            # if int(cur_time // 0.5) < 1:
            #     cv2.imwrite(f"images/scr{photo_counter}.jpg", frame)
    
    def get_photo(self):
        
    # def frames_cutter(self, frame):
    #     frame_index = 0
    #     while rval:    
    #         frame_index += 1
    #         print(frame_index)
    #         cv2.imshow("webcam", frame)
    #         rval, frame = self.capture.read()
    #         key = cv2.waitKey(20)
    #         if frame_index % 10 == 0:
    #             cv2.imwrite(f"images/scr{frame_index}.jpg", frame)
    #         if frame_index == 100:
    #             break
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())
