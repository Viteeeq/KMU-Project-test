import numpy as np
from typing import List, Tuple, Optional
import pickle
from concurrent.futures import ThreadPoolExecutor

class KDNode:
    def __init__(self, face_data: np.ndarray, user_id: str, 
                 left: Optional['KDNode'] = None, 
                 right: Optional['KDNode'] = None,
                 axis: int = 0):
        self.face_data = face_data
        self.user_id = user_id
        self.left = left
        self.right = right
        self.axis = axis
        # Добавляем кэш для ускорения поиска
        self.median_value = float(np.median(face_data, axis=0)[axis])
        self.norm = np.linalg.norm(face_data)

class KDTree:
    def __init__(self):
        self.root: Optional[KDNode] = None
        self.size = 0
        self.dimension = 0
        
    def _build_tree(self, faces: List[Tuple[np.ndarray, str]], 
                   start: int, end: int, axis: int) -> Optional[KDNode]:
        """Рекурсивно строит k-d дерево с улучшенной балансировкой"""
        if start >= end:
            return None
            
        faces_slice = faces[start:end]
        
        # Выбираем ось с наибольшей дисперсией для лучшей балансировки
        if len(faces_slice) > 1:
            variances = np.var([x[0] for x in faces_slice], axis=0)
            axis = np.argmax(variances)
        
        # Сортируем по медиане выбранной оси
        faces_sorted = sorted(faces_slice, 
                            key=lambda x: np.median(x[0], axis=0)[axis])
        median_idx = len(faces_sorted) // 2
        
        # Создаем узел с предвычисленными значениями
        node = KDNode(faces_sorted[median_idx][0], 
                     faces_sorted[median_idx][1],
                     axis=axis)
        
        faces[start:end] = faces_sorted
        mid = start + median_idx
        
        # Рекурсивно строим поддеревья
        node.left = self._build_tree(faces, start, mid, 
                                   (axis + 1) % self.dimension)
        node.right = self._build_tree(faces, mid + 1, end,
                                    (axis + 1) % self.dimension)
        
        return node
        
    def build(self, faces: List[Tuple[np.ndarray, str]]) -> None:
        """Строит k-d дерево из списка лиц"""
        if not faces:
            return
            
        self.dimension = faces[0][0].shape[1]
        self.root = self._build_tree(faces, 0, len(faces), 0)
        self.size = len(faces)
        
    def _find_nearest(self, node: Optional[KDNode], 
                     target: np.ndarray,
                     best_dist: float = float('inf'),
                     best_node: Optional[KDNode] = None) -> Tuple[float, Optional[KDNode]]:
        """Рекурсивно находит ближайшее лицо с оптимизированным поиском"""
        if node is None:
            return best_dist, best_node
            
        # Используем косинусное расстояние для лучшей точности
        target_norm = np.linalg.norm(target)
        current_dist = 1 - np.dot(node.face_data.flatten(), target.flatten()) / \
                      (node.norm * target_norm)
        
        if current_dist < best_dist:
            best_dist = current_dist
            best_node = node
            
        # Используем предвычисленное медианное значение
        target_val = np.median(target, axis=0)[node.axis]
        
        if target_val < node.median_value:
            first, second = node.left, node.right
        else:
            first, second = node.right, node.left
            
        # Рекурсивно ищем в первом поддереве
        best_dist, best_node = self._find_nearest(first, target, 
                                                best_dist, best_node)
        
        # Улучшенная проверка необходимости поиска во втором поддереве
        axis_dist = abs(target_val - node.median_value)
        if axis_dist < best_dist * 1.5:  # Увеличенный порог для более точного поиска
            best_dist, best_node = self._find_nearest(second, target,
                                                    best_dist, best_node)
        
        return best_dist, best_node
        
    def find_nearest(self, target: np.ndarray) -> Tuple[Optional[str], float]:
        """Находит ближайшее лицо к целевому"""
        if self.root is None:
            return None, float('inf')
            
        _, best_node = self._find_nearest(self.root, target)
        if best_node is None:
            return None, float('inf')
            
        # Вычисляем финальное расстояние
        final_dist = 1 - np.dot(best_node.face_data.flatten(), target.flatten()) / \
                    (best_node.norm * np.linalg.norm(target))
        return best_node.user_id, final_dist
        
    def save(self, filepath: str) -> None:
        """Сохраняет k-d дерево в файл"""
        if self.root is None:
            return
            
        with open(filepath, 'wb') as f:
            pickle.dump(self.root, f)
            
    def load(self, filepath: str) -> None:
        """Загружает k-d дерево из файла"""
        try:
            with open(filepath, 'rb') as f:
                self.root = pickle.load(f)
                # Подсчитываем размер дерева и определяем размерность
                def count_nodes(node: Optional[KDNode]) -> int:
                    if node is None:
                        return 0
                    if self.dimension == 0:
                        self.dimension = node.face_data.shape[1]
                    return 1 + count_nodes(node.left) + count_nodes(node.right)
                self.size = count_nodes(self.root)
        except FileNotFoundError:
            self.root = None
            self.size = 0 