import cv2
import numpy as np
from deepface import DeepFace
from sklearn.neighbors import KDTree
from typing import Tuple, List, Dict, Optional
import time

class BiometricProcessor:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.kdtree = None
        self.face_encodings = []
        self.user_ids = []

    def extract_face_features(self, image_path: str) -> Optional[Tuple[np.ndarray, Dict]]:
        """
        Извлекает признаки лица из изображения с помощью DeepFace
        """
        try:
            # Загружаем изображение
            img = cv2.imread(image_path)
            if img is None:
                print(f"Не удалось загрузить изображение: {image_path}")
                return None

            # Получаем признаки с помощью DeepFace
            result = DeepFace.analyze(img, 
                                    actions=['age', 'gender', 'race', 'emotion'],
                                    enforce_detection=False)
            
            if not result:
                return None

            # Извлекаем лицо и конвертируем в оттенки серого
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) == 0:
                return None

            # Берем первое обнаруженное лицо
            (x, y, w, h) = faces[0]
            face = gray[y:y+h, x:x+w]
            
            # Нормализуем размер лица
            face = cv2.resize(face, (100, 100))
            
            # Получаем метаданные
            metadata = {
                'age': result[0]['age'],
                'gender': result[0]['gender'],
                'race': result[0]['dominant_race'],
                'emotion': result[0]['dominant_emotion']
            }

            return face, metadata

        except Exception as e:
            print(f"Ошибка при обработке изображения: {str(e)}")
            return None

    def build_kdtree(self, face_encodings: List[np.ndarray], user_ids: List[str]):
        """
        Строит k-d дерево для быстрого поиска похожих лиц
        """
        self.face_encodings = face_encodings
        self.user_ids = user_ids
        self.kdtree = KDTree(face_encodings)

    def find_similar_faces_kdtree(self, face_encoding: np.ndarray, 
                                k: int = 5, 
                                threshold: float = 0.6) -> List[Tuple[str, float]]:
        """
        Ищет похожие лица с помощью k-d дерева
        """
        if self.kdtree is None:
            return []

        # Находим k ближайших соседей
        distances, indices = self.kdtree.query([face_encoding], k=k)
        
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            similarity = 1 - (distance / np.sqrt(2))  # Нормализуем расстояние
            if similarity > threshold:
                results.append((self.user_ids[idx], similarity))

        return results

    def compare_faces(self, face1: np.ndarray, face2: np.ndarray) -> float:
        """
        Сравнивает два лица и возвращает степень схожести
        """
        # Приводим лица к одинаковому размеру
        face1 = cv2.resize(face1, (100, 100))
        face2 = cv2.resize(face2, (100, 100))
        
        # Вычисляем разницу между лицами
        diff = cv2.absdiff(face1, face2)
        mean_diff = np.mean(diff)
        
        # Преобразуем разницу в схожесть (0-1)
        similarity = 1 - (mean_diff / 255.0)
        return similarity

    def benchmark_search(self, face_encoding: np.ndarray, 
                        database_size: int,
                        k: int = 5) -> Dict[str, float]:
        """
        Проводит тестирование производительности разных методов поиска
        """
        results = {}
        
        # Тест k-d дерева
        start_time = time.time()
        kdtree_results = self.find_similar_faces_kdtree(face_encoding, k=k)
        kdtree_time = time.time() - start_time
        
        results['kdtree'] = {
            'time': kdtree_time,
            'results': kdtree_results
        }
        
        return results 