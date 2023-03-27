import sys
from PyQt5.QtWidgets import (QWidget, QListWidget, QVBoxLayout, QApplication)



class Example(QWidget):
    def __init__(self, items):
        super().__init__()

        self.lists = (items)
        self.l = QListWidget()
        self.l.addItems(self.lists)

        self.l.itemClicked.connect(self.selectionChanged)

        vbox = QVBoxLayout()
        vbox.addWidget(self.l)
        self.setLayout(vbox)

    def selectionChanged(self, item):
        print("Вы кликнули: {}".format(item.text()))
        if item.text()=="item2": print("Делайте что-нибудь.")
        # ...

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example([])
    ex.show()
    sys.exit(app.exec_())