import sys
import sys
import cv2
import time
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QPushButton, QGridLayout, QWidget, QMainWindow, QListWidget, QVBoxLayout
from database import PostamatDatabase
import image


class Game(QWidget):
    def __init__(self, s, r, f, d, items, parent):
        super(Game, self).__init__()

        print(s, r, f, d, items, parent)
        self.parent = parent

        # self.label = QLabel()
        # self.label.setPixmap(QPixmap(img))

        self.button = QPushButton('End', clicked=self.go_end)
        self.grid_layout = QGridLayout(self)
        self.items = items
        self.check_items = {}
        for i in range(len(self.items)):
            self.check_items[i] = self.items[i]
        self.lists = (self.items)
        self.l = QListWidget()
        self.l.addItems(self.lists)
        self.l.setGeometry(100, 100, 680, 480)
        self.grid_layout.addWidget(self.l)
        self.grid_layout.addWidget(self.button)

        self.l.itemClicked.connect(self.selectionChanged)

        self.grid_layout.addWidget(self.l)

    def selectionChanged(self, item):
        print("Вы кликнули: {}".format(item.text()))
        itm_txt = item.text()
        print("Делайте что-нибудь.", itm_txt)
        print(self.check_items)
        print(item)
        res = None
        for k, v in self.check_items.items():
            if v == itm_txt:
                res = int(k)
        self.hide()
        self.l.clear()
        self.std_choose = "(Выбрано)"
        if self.std_choose in self.lists[res]:
            self.lists[res] = self.lists[res].replace(self.std_choose, '')
        else:
            self.lists[res] += self.std_choose
        for i in range(len(self.lists)):
            self.check_items[i] = self.lists[i]
        self.l.addItems(self.lists)
        self.check_items
        self.show()
        
    def go_end(self):
        self.parent.show()        
        self.hide()
        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        self.button = QPushButton('Start', clicked=self.go_start)

        self.grid_layout = QGridLayout(centralWidget)
        ###
        self.db = PostamatDatabase('postamat.db')
        self.db.create_table()
        self.name = "randomname"
        self.ImPr = image.ImageProcessing()

        # Создаем QLabel для отображения видео
        self.label = QLabel(self)
        self.label.setGeometry(100, 100, 680, 480)
        self.grid_layout.addWidget(self.label)

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
        self.grid_layout.addWidget(self.snap_btn)
        self.snap_btn.clicked.connect(self.verification)
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

    def go_start(self, items):
        self.g = Game('s','r','f','d', items, self)
        self.g.show()        
        self.hide()
        
    def take_snapshot(self):
        # Считываем текущий кадр из видеопотока
        start_time = time.time()
        ret, frame = self.capture.read()

        # Сохраняем кадр в файл
        if ret:
            cv2.imwrite(f'{self.name}.jpg', frame)
            return start_time
        
    def verification(self):
        try:
            user_name, user_items = self.ImPr.faces_comparing(self.take_snapshot())
            print(user_items.split(','))
            print(type(user_items.split(',')))
            user_items_ready = user_items.split(',')
            self.go_start(user_items_ready)
        except:
            pass

if __name__=="__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()