import cv2
import numpy as np
from typing import List, Tuple, Optional
import os
from database import BiometricDatabase

class FaceProcessor:
    def __init__(self):
        """Инициализация процессора лиц"""
        # Загружаем каскадный классификатор для обнаружения лиц
        cascade_path = 'haarcascade_frontalface_default.xml'
        if not os.path.exists(cascade_path):
            raise FileNotFoundError(f"Файл каскадного классификатора не найден: {cascade_path}")
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        # Инициализируем базу данных
        self.db = BiometricDatabase()
        
    def detect_face(self, image: np.ndarray) -> Optional[np.ndarray]:
        """Обнаружение лица на изображении"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return None
            
        # Берем первое обнаруженное лицо
        x, y, w, h = faces[0]
        face = gray[y:y+h, x:x+w]
        
        # Нормализуем размер
        face = cv2.resize(face, (100, 100))
        
        return face
        
    def add_face(self, face: np.ndarray, user_id: str) -> None:
        """Добавление лица в базу данных"""
        if face is None:
            raise ValueError("Лицо не обнаружено на изображении")
            
        self.db.add_face(user_id, face)
        
    def recognize_face(self, face: np.ndarray) -> Optional[str]:
        """Распознавание лица с использованием линейного поиска"""
        if face is None:
            return None
            
        # Получаем все лица из базы данных
        faces = self.db.get_all_faces()
        
        best_match = None
        min_distance = float('inf')
        
        # Линейный поиск
        for user_id, stored_face in faces:
            # Вычисляем расстояние между лицами
            distance = np.linalg.norm(face - stored_face)
            
            if distance < min_distance:
                min_distance = distance
                best_match = user_id
                
        return best_match if min_distance < 1000 else None
        
    def clear_database(self) -> None:
        """Очистка базы данных"""
        self.db.clear_database()
        
    def _retrain_recognizer(self) -> None:
        """
        Переобучает распознаватель лиц
        """
        faces = []
        labels = []
        
        face_dir = 'faces'
        if not os.path.exists(face_dir):
            return
            
        for filename in os.listdir(face_dir):
            if filename.endswith('.jpg'):
                user_id = filename[:-4]
                if user_id in self.face_labels:
                    face = cv2.imread(os.path.join(face_dir, filename), cv2.IMREAD_GRAYSCALE)
                    faces.append(face)
                    labels.append(self.face_labels[user_id])
                    
        if faces and labels:
            self.face_recognizer.train(faces, np.array(labels))
            self.face_recognizer.save('face_recognizer.yml')
            
    def get_face_features(self, face: np.ndarray) -> np.ndarray:
        """
        Извлекает признаки лица для сравнения
        """
        # Нормализация размера
        face = cv2.resize(face, (100, 100))
        
        # Гистограмма градиентов
        hog = cv2.HOGDescriptor()
        features = hog.compute(face)
        
        return features
        
    def compare_faces(self, face1: np.ndarray, face2: np.ndarray) -> float:
        """
        Сравнивает два лица и возвращает степень схожести
        """
        features1 = self.get_face_features(face1)
        features2 = self.get_face_features(face2)
        
        # Евклидово расстояние между признаками
        distance = np.linalg.norm(features1 - features2)
        similarity = 1.0 / (1.0 + distance)
        
        return similarity 