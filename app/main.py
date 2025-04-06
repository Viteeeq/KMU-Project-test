import sys
import cv2
import numpy as np
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                           QMessageBox, QStackedWidget)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap
from face_processor import FaceProcessor
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Система распознавания лиц")
        self.setGeometry(100, 100, 800, 600)
        
        # Инициализация процессора лиц
        self.face_processor = FaceProcessor()
        
        # Создание центрального виджета
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Создание основного layout
        self.layout = QVBoxLayout(self.central_widget)
        
        # Создание стека виджетов
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)
        
        # Создание страниц
        self.main_page = QWidget()
        self.registration_page = QWidget()
        self.verification_page = QWidget()
        
        # Добавление страниц в стек
        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.registration_page)
        self.stacked_widget.addWidget(self.verification_page)
        
        # Настройка страниц
        self.setup_main_page()
        self.setup_registration_page()
        self.setup_verification_page()
        
        # Инициализация камеры
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        
    def setup_main_page(self):
        layout = QVBoxLayout(self.main_page)
        
        # Кнопки навигации
        register_btn = QPushButton("Регистрация")
        verify_btn = QPushButton("Верификация")
        
        register_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.registration_page))
        verify_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.verification_page))
        
        layout.addWidget(register_btn)
        layout.addWidget(verify_btn)
        
    def setup_registration_page(self):
        layout = QVBoxLayout(self.registration_page)
        
        # Виджет для отображения видео
        self.registration_video = QLabel()
        self.registration_video.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.registration_video)
        
        # Поле ввода ID пользователя
        self.user_id_input = QLineEdit()
        self.user_id_input.setPlaceholderText("Введите ID пользователя")
        layout.addWidget(self.user_id_input)
        
        # Кнопки
        register_btn = QPushButton("Зарегистрировать")
        back_btn = QPushButton("Назад")
        
        register_btn.clicked.connect(self.register_user)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.main_page))
        
        layout.addWidget(register_btn)
        layout.addWidget(back_btn)
        
    def setup_verification_page(self):
        layout = QVBoxLayout(self.verification_page)
        
        # Виджет для отображения видео
        self.verification_video = QLabel()
        self.verification_video.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.verification_video)
        
        # Кнопки
        verify_btn = QPushButton("Проверить")
        back_btn = QPushButton("Назад")
        
        verify_btn.clicked.connect(self.verify_user)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.main_page))
        
        layout.addWidget(verify_btn)
        layout.addWidget(back_btn)
        
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Конвертируем кадр в RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Обнаруживаем лицо
            face_result = self.face_processor.detect_face(frame)
            if face_result:
                face, (x, y, w, h) = face_result
                # Рисуем прямоугольник вокруг лица
                cv2.rectangle(rgb_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Конвертируем в QImage и отображаем
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            
            # Отображаем на соответствующей странице
            current_page = self.stacked_widget.currentWidget()
            if current_page == self.registration_page:
                self.registration_video.setPixmap(QPixmap.fromImage(qt_image))
            elif current_page == self.verification_page:
                self.verification_video.setPixmap(QPixmap.fromImage(qt_image))
                
    def register_user(self):
        user_id = self.user_id_input.text()
        if not user_id:
            QMessageBox.warning(self, "Ошибка", "Введите ID пользователя")
            return
            
        ret, frame = self.cap.read()
        if ret:
            face_result = self.face_processor.detect_face(frame)
            if face_result:
                face, _ = face_result
                self.face_processor.add_face(face, user_id)
                QMessageBox.information(self, "Успех", "Пользователь успешно зарегистрирован")
            else:
                QMessageBox.warning(self, "Ошибка", "Лицо не обнаружено")
                
    def verify_user(self):
        ret, frame = self.cap.read()
        if ret:
            face_result = self.face_processor.detect_face(frame)
            if face_result:
                face, _ = face_result
                user_id = self.face_processor.recognize_face(face)
                if user_id:
                    QMessageBox.information(self, "Успех", f"Пользователь распознан: {user_id}")
                else:
                    QMessageBox.warning(self, "Ошибка", "Пользователь не распознан")
            else:
                QMessageBox.warning(self, "Ошибка", "Лицо не обнаружено")
                
    def showEvent(self, event):
        self.timer.start(30)  # Обновление каждые 30 мс
        
    def closeEvent(self, event):
        self.timer.stop()
        self.cap.release()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())