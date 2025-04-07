import cv2
import numpy as np
from typing import Tuple, List, Optional
import os
from app.database import BiometricDatabase
from app.kd_tree import KDTree

class OptimizedFaceProcessor:
    def __init__(self):
        """Инициализация процессора лиц"""
        # Загружаем каскадный классификатор
        cascade_path = 'haarcascade_frontalface_default.xml'
        if not os.path.exists(cascade_path):
            raise FileNotFoundError(f"Файл каскадного классификатора не найден: {cascade_path}")
            
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        if self.face_cascade.empty():
            raise ValueError("Не удалось загрузить каскадный классификатор")
            
        # Инициализируем базу данных
        self.db = BiometricDatabase()
        
        # Инициализируем k-d дерево
        self.kd_tree = KDTree()
        
        # Загружаем существующие лица в k-d дерево
        self._load_faces_to_tree()
        
    def _load_faces_to_tree(self) -> None:
        """Загружает лица из базы данных в k-d дерево"""
        faces = self.db.get_all_faces()
        if faces:
            # Преобразуем данные в формат для k-d дерева
            tree_data = [(face_data, user_id) for user_id, face_data in faces]
            self.kd_tree.build(tree_data)
            
    def detect_face(self, image: np.ndarray) -> Optional[np.ndarray]:
        """Обнаруживает лицо на изображении"""
        if image is None or image.size == 0:
            return None
            
        # Преобразуем изображение в оттенки серого
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Обнаруживаем лица
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        if len(faces) == 0:
            return None
            
        # Берем первое обнаруженное лицо
        x, y, w, h = faces[0]
        face = gray[y:y+h, x:x+w]
        
        # Нормализуем размер
        face = cv2.resize(face, (100, 100))
        
        # Нормализуем значения
        face = face.astype(np.float32) / 255.0
        
        return face
        
    def add_face(self, face: np.ndarray, user_id: str) -> bool:
        """Добавляет лицо в базу данных и k-d дерево"""
        if face is None or face.size == 0:
            return False
            
        # Добавляем в базу данных
        if not self.db.add_face(user_id, face):
            return False
            
        # Добавляем в k-d дерево
        faces = self.db.get_all_faces()
        tree_data = [(face_data, uid) for uid, face_data in faces]
        self.kd_tree.build(tree_data)
        
        return True
        
    def recognize_face(self, face: np.ndarray) -> Tuple[Optional[str], float]:
        """Распознает лицо с использованием k-d дерева"""
        if face is None or face.size == 0:
            return None, float('inf')
            
        # Находим ближайшее лицо в k-d дереве
        user_id, distance = self.kd_tree.find_nearest(face)
        
        # Если расстояние слишком большое, считаем что лицо не найдено
        if distance > 0.6:  # Пороговое значение
            return None, float('inf')
            
        return user_id, distance
        
    def save_state(self) -> None:
        """Сохраняет состояние процессора"""
        self.kd_tree.save('kd_tree.pkl')
        
    def load_state(self) -> None:
        """Загружает состояние процессора"""
        self.kd_tree.load('kd_tree.pkl') 