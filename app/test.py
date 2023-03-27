import sys
from app import VideoPlayer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QStackedWidget

class Window1(QWidget):
    def __init__(self):
        super().__init__()
        self.button = QPushButton('Go to Window 2', self)
        self.button.setGeometry(800, 100, 120, 50)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        self.button.clicked.connect(self.go_to_window2)

    def go_to_window2(self):
        stacked_widget.setCurrentWidget(window2)

class Window2(QWidget):
    def __init__(self):
        super().__init__()
        self.button = QPushButton('Go to Window 1', self)
        self.button.setGeometry(60, 100, 120, 50)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        self.button.clicked.connect(self.go_to_window1)

    def go_to_window1(self):
        stacked_widget.setCurrentWidget(window1)

app = QApplication(sys.argv)
stacked_widget = QStackedWidget()
window1 = VideoPlayer()
window2 = Window2()
stacked_widget.addWidget(window1)
stacked_widget.addWidget(window2)
# stacked_widget.setCurrentWidget(window1)
stacked_widget.show()
sys.exit(app.exec_())