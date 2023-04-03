from PyQt5.QtWidgets import QMessageBox


def alert(self, str, call_code):
    dlg = QMessageBox(self)
    dlg.setWindowTitle("Предупреждение")
    if call_code == 1:
        dlg.setText(f"Вы взяли:\n{str}")
    elif call_code == 2:
        dlg.setText(f"Вы вернули:\n{str}")
    button = dlg.exec()
    if button == QMessageBox.Ok:
        print("OK!")