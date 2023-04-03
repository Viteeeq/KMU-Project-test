import sys
import sys
import cv2
import time
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QGridLayout, QWidget, QMainWindow, QListWidget, QMessageBox
from database import PostamatDatabase
import image
from alerts import alert

class ReturnWindow(QWidget):
    def __init__(self, name, db, parent):
        super(ReturnWindow, self).__init__()
        
        self.db = db
        self.user = name
        self.parent = parent
        self.items = self.db.get_items(self.user).split(',')
        self.std_choose = "(Выбрано)"
        self.std2 = '   '
        self.items_copy = []
        for i in range(len(self.items)):
            if (self.std_choose in self.items[i]):
                self.items_copy.append(self.items[i].replace(self.std_choose, '', 1))

        self.setWindowTitle(f'Что вы хотите вернуть?')
        self.setFixedSize(640, 480)
        self.return_button = QPushButton('Вернуть', clicked = self.return_items)
        self.exit_button = QPushButton('Выход', clicked=self.step_back)
        self.grid_layout2 = QGridLayout(self)
        self.rlist = QListWidget()
        self.check_items2 = {}
        for i in range(len(self.items_copy)):
            x = self.items_copy[i]
            self.check_items2[i] = self.items_copy[i]
            self.rlist.addItem(x)
        self.grid_layout2.addWidget(self.rlist)
        self.grid_layout2.addWidget(self.return_button)
        self.grid_layout2.addWidget(self.exit_button)

        self.rlist.itemClicked.connect(self.select_one)
        
    def select_one(self, item):
        # print("Вы кликнули: {}".format(item.text()))
        itm_txt = item.text()
        res = None
        for k, v in self.check_items2.items():
            if v == itm_txt:
                res = int(k)
        self.hide()
        self.rlist.clear()
        if self.std_choose in self.items_copy[res]:
            self.items_copy[res] = self.items_copy[res].replace(self.std_choose, '')
        else:
            self.items_copy[res] = self.std_choose + self.items_copy[res]
        for i in range(len(self.items_copy)):
            self.check_items2[i] = self.items_copy[i]
        self.rlist.addItems(self.items_copy)
        # print(self.check_items2)
        # print(self.items_copy)
        self.show()
        
    def return_items(self):
        for i in range(len(self.items)):
            if self.items[i] in self.items_copy:
                self.items[i] = self.items[i].replace(self.std_choose, '')
        # print(self.items)
        str1 = ''
        for item in self.items:
            str1 += item + ','
            # print(item)
        str1 = str1[:-1]
        print(str1, '- return')
        self.db.change_items(self.user, str1)
        self.end_return()
        
    def step_back(self):
        self.parent.show()
        self.hide()
        
    def end_return(self):
        self.parent.parent.show()
        self.hide()


class SelectionWindow(QWidget):
    def __init__(self, name, db, parent):
        super(SelectionWindow, self).__init__()
        
        self.db = db
        self.user = name
        self.parent = parent
        self.items = self.db.get_items(self.user).split(',')
        self.std_choose = "(Выбрано)"
        self.check_items = {}
        self.items_copy = []

        self.setWindowTitle(f'Предметы {self.user}')
        self.setFixedSize(640, 480)
        self.get_button = QPushButton('Забрать', clicked=self.go_end)
        self.take_button = QPushButton('Выбрать всё', clicked=self.select_all)
        self.return_button = QPushButton('Вернуть', clicked=self.go_to_return)
        self.grid_layout = QGridLayout(self)
        self.l = QListWidget()
        for i in range(len(self.items)):
            if not(self.std_choose in self.items[i]):
                self.items_copy.append(self.items[i])
        # print(self.items_copy)
        for i in range(len(self.items_copy)):
            x = self.items_copy[i]
            self.check_items[i] = x
            self.l.addItem(x)
        self.grid_layout.addWidget(self.l)
        self.grid_layout.addWidget(self.get_button)
        self.grid_layout.addWidget(self.take_button)
        self.grid_layout.addWidget(self.return_button)
        
        self.l.itemClicked.connect(self.select_one)

    def select_one(self, item):
        # print("Вы кликнули: {}".format(item.text()))
        itm_txt = item.text()
        res = None
        for k, v in self.check_items.items():
            if v == itm_txt:
                res = int(k)
        self.hide()
        self.l.clear()
        if self.std_choose in self.items_copy[res]:
            self.items_copy[res] = self.items_copy[res].replace(self.std_choose, '')
        else:
            self.items_copy[res] = self.std_choose + self.items_copy[res]
        for i in range(len(self.items_copy)):
            self.check_items[i] = self.items_copy[i]
        self.l.addItems(self.items_copy)
        self.show()
        
    def go_end(self):
        str_for_db = ''
        str_for_alert = ''
        for i in range(len(self.items_copy)):
            if not(self.items_copy[i] in self.items):
                self.items[self.items.index(self.items_copy[i][len(self.std_choose):])] = self.items_copy[i]
                str_for_alert += self.items_copy[i][len(self.std_choose):] + '\n'
        for i in range(len(self.items)):
            str_for_db += self.items[i] + ','
        str_for_db = str_for_db[:-1]
        self.db.change_items(self.user, str_for_db)
        alert(self, str_for_alert)
            
        self.parent.show()
        self.hide()
        
    def select_all(self):
        for x in range(self.l.count()):
            self.select_one(self.l.item(x))
    
    def go_to_return(self):
        self.s = ReturnWindow(self.user, self.db, self)
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
        self.setWindowTitle('Система доступа к ячейкам хранения')

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
        self.g = SelectionWindow(username, self.db, self)
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
            # print(user_items.split(','))
            user_items_ready = user_items.split(',')
            self.go_to_selection(user_items_ready, user_name)
        except:
            pass

if __name__=="__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()