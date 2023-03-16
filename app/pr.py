import sys
from PyQt5.QtWidgets import QApplication, QMainWindow


class ParentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100*4, 100*4, 400*4, 300*4)
        self.setWindowTitle("Parent Window")


class WindowToCenter(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.setWindowTitle("Window To Center")
        self.setGeometry(0, 0, 200, 150)
        self.move(parent.frameGeometry().width()/2 - self.frameSize().width()/2, parent.frameGeometry().height()/2 - self.frameSize().height()/2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    parent_window = ParentWindow()
    window_to_center = WindowToCenter(parent_window)
    window_to_center.show()
    sys.exit(app.exec_())
