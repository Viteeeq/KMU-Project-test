from PyQt5.QtWidgets import QMessageBox


def alert(self, str):
    dlg = QMessageBox(self)
    dlg.setWindowTitle("Предупреждение")
    dlg.setText(f"Вы взяли:\n{str}")
    button = dlg.exec()
    if button == QMessageBox.Ok:
        print("OK!")