import os
import cv2
import numpy as np
from typing import List, Tuple
import random

class DataGenerator:
    def __init__(self, output_dir: str = 'test_data'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_face_image(self, size: Tuple[int, int] = (100, 100)) -> np.ndarray:
        """
        Генерирует синтетическое изображение лица
        """
        # Создаем базовое изображение
        img = np.zeros((size[0], size[1]), dtype=np.uint8)
        
        # Добавляем случайный шум
        noise = np.random.normal(0, 25, size).astype(np.uint8)
        img = cv2.add(img, noise)
        
        # Добавляем овальную форму лица
        center = (size[0]//2, size[1]//2)
        axes = (size[0]//3, size[1]//4)
        cv2.ellipse(img, center, axes, 0, 0, 360, 255, -1)
        
        # Добавляем глаза
        eye_size = (size[0]//8, size[1]//12)
        left_eye = (center[0] - size[0]//6, center[1] - size[1]//8)
        right_eye = (center[0] + size[0]//6, center[1] - size[1]//8)
        cv2.ellipse(img, left_eye, eye_size, 0, 0, 360, 0, -1)
        cv2.ellipse(img, right_eye, eye_size, 0, 0, 360, 0, -1)
        
        # Добавляем рот
        mouth_size = (size[0]//4, size[1]//8)
        mouth_center = (center[0], center[1] + size[1]//6)
        cv2.ellipse(img, mouth_center, mouth_size, 0, 0, 180, 0, -1)
        
        return img

    def add_variations(self, img: np.ndarray) -> np.ndarray:
        """
        Добавляет случайные вариации к изображению
        """
        # Случайное освещение
        brightness = random.uniform(0.8, 1.2)
        img = cv2.multiply(img, brightness)
        
        # Случайный контраст
        contrast = random.uniform(0.8, 1.2)
        img = cv2.multiply(img, contrast)
        
        # Случайный шум
        noise = np.random.normal(0, 5, img.shape).astype(np.uint8)
        img = cv2.add(img, noise)
        
        return img

    def generate_face(self) -> np.ndarray:
        """
        Генерирует одно лицо с вариациями
        """
        face = self.generate_face_image()
        face = self.add_variations(face)
        # Нормализуем значения
        face = face.astype(np.float32) / 255.0
        # Преобразуем в 2D массив
        face = face.reshape(100, 100)
        return face

    def generate_faces(self, num_faces: int) -> List[np.ndarray]:
        """
        Генерирует список лиц
        """
        return [self.generate_face() for _ in range(num_faces)]

    def generate_dataset(self, 
                        num_users: int,
                        variations_per_user: int = 5) -> List[str]:
        """
        Генерирует набор тестовых данных
        """
        image_paths = []
        
        for user_id in range(num_users):
            # Создаем базовое изображение лица
            base_face = self.generate_face_image()
            
            # Сохраняем базовое изображение
            base_path = os.path.join(self.output_dir, f'user_{user_id}_base.jpg')
            cv2.imwrite(base_path, base_face)
            image_paths.append(base_path)
            
            # Генерируем вариации
            for var_id in range(variations_per_user):
                var_face = self.add_variations(base_face.copy())
                var_path = os.path.join(self.output_dir, 
                                      f'user_{user_id}_var_{var_id}.jpg')
                cv2.imwrite(var_path, var_face)
                image_paths.append(var_path)
        
        return image_paths

    def generate_test_sets(self, 
                          sizes: List[int] = [100, 500, 1000, 5000, 10000],
                          variations_per_user: int = 5):
        """
        Генерирует несколько наборов тестовых данных разного размера
        """
        for size in sizes:
            print(f"Генерация набора данных размером {size}")
            output_dir = os.path.join(self.output_dir, f'size_{size}')
            os.makedirs(output_dir, exist_ok=True)
            
            self.output_dir = output_dir
            self.generate_dataset(size, variations_per_user)

if __name__ == "__main__":
    generator = DataGenerator()
    generator.generate_test_sets() 