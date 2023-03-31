import sys
import sys
import cv2
import time
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QPushButton, QGridLayout, QWidget, QMainWindow, QListWidget
from database import PostamatDatabase
import image

class ReturnWindow(QWidget):
    def __init__(self, items, name, db, parent):
        super(ReturnWindow, self).__init__()
        
        self.db = db
        self.user = name
        self.parent = parent
        self.items = self.db.get_items(self.user).split(',')
        self.std_choose = "(Выбрано)"
        self.std2 = '+++'

        self.return_button = QPushButton('Вернуть', clicked = self.return_items)
        self.exit_button = QPushButton('Выход', clicked=self.go_end)
        self.grid_layout2 = QGridLayout(self)
        self.rlist = QListWidget()
        self.check_items2 = {}
        for i in range(len(self.items)):
            x = self.items[i]
            self.check_items2[i] = self.items[i]
            if (self.std_choose in x):
                self.rlist.addItem(x)
        # self.rlist.addItems(self.items)
        # self.l.addItem(self.items[i])
        self.grid_layout2.addWidget(self.rlist)
        self.grid_layout2.addWidget(self.return_button)
        self.grid_layout2.addWidget(self.exit_button)

        self.rlist.itemClicked.connect(self.select_one)
        
    def select_one(self, item):
        print("Вы кликнули: {}".format(item.text()))
        itm_txt = item.text()
        res = None
        for k, v in self.check_items2.items():
            if v == itm_txt:
                res = int(k)
        self.hide()
        self.rlist.clear()
        if self.std2 in self.items[res]:
            self.items[res] = self.items[res].replace(self.std2, '')
        else:
            self.items[res] = self.std2 + self.items[res]
        for i in range(len(self.items)):
            self.check_items2[i] = self.items[i]
        # self.rlist.addItems(self.items)
        for i in range(len(self.items)):
            x = self.items[i]
            self.check_items2[i] = self.items[i]
            if (self.std_choose in x):
                self.rlist.addItem(x)
        print(self.check_items2)
        self.show()
        
    def return_items(self):
        print(self.items)
    
    def go_end(self):
        self.parent.show()
        self.hide()


class SelectionWindow(QWidget):
    def __init__(self, items, name, db, parent):
        super(SelectionWindow, self).__init__()
        
        self.db = db
        self.user = name
        self.parent = parent
        self.items = items
        self.items_copy = self.items
        self.std_choose = "(Выбрано)"
        self.check_items = {}

        self.get_button = QPushButton('Забрать', clicked=self.go_end)
        self.take_button = QPushButton('Выбрать всё', clicked=self.select_all)
        self.return_button = QPushButton('Вернуть', clicked=self.go_to_return)
        self.grid_layout = QGridLayout(self)
        self.l = QListWidget()
        for i in range(len(self.items)):
            x = self.items[i]
            self.check_items[i] = self.items[i]
            if not(self.std_choose in x):
                self.l.addItem(x)
        # self.l.addItems(self.items)
        self.grid_layout.addWidget(self.l)
        self.grid_layout.addWidget(self.get_button)
        self.grid_layout.addWidget(self.take_button)
        self.grid_layout.addWidget(self.return_button)
        
        self.l.itemClicked.connect(self.select_one)

    def select_one(self, item):
        print("Вы кликнули: {}".format(item.text()))
        itm_txt = item.text()
        res = None
        for k, v in self.check_items.items():
            if v == itm_txt:
                res = int(k)
        self.hide()
        self.l.clear()
        if self.std_choose in self.items[res]:
            self.items[res] = self.items[res].replace(self.std_choose, '')
        else:
            self.items[res] = self.std_choose + self.items[res]
        for i in range(len(self.items)):
            self.check_items[i] = self.items[i]
        self.l.addItems(self.items)
        print(self.check_items)
        self.show()
        
    def go_end(self):
        str1 = ''
        for k, v in self.check_items.items():
            str1 += v + ','
            print(k, ' ',v)
        str1 = str1[:-1]
        print(str1)
        self.db.change_items(self.user, str1)
        self.parent.show()
        self.hide()
        
    def select_all(self):
        self.hide()
        self.l.clear()
        for i in range(len(self.items)):
            if not(self.std_choose in self.items[i]):
                self.items[i] = self.std_choose + self.items[i]
        for i in range(len(self.items)):
            self.check_items[i] = self.items[i]
        self.l.addItems(self.items)
        self.show()
    
    def go_to_return(self):
        self.s = ReturnWindow(self.items, self.user, self.db, self)
        self.s.show()        
        self.hide()
        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        self.button = QPushButton('Верификация', clicked=self.go_to_selection)

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

    def go_to_selection(self, items, username):
        self.g = SelectionWindow(items, username, self.db, self)
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
            self.go_to_selection(user_items_ready, user_name)
        except:
            pass

if __name__=="__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()