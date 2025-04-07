import numpy as np
from typing import List, Tuple, Optional
import pickle

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

class KDTree:
    def __init__(self):
        self.root: Optional[KDNode] = None
        self.size = 0
        
    def _build_tree(self, faces: List[Tuple[np.ndarray, str]], 
                   start: int, end: int, axis: int) -> Optional[KDNode]:
        """Рекурсивно строит k-d дерево"""
        if start >= end:
            return None
            
        # Находим медиану по текущей оси
        faces_slice = faces[start:end]
        # Используем среднее значение по оси для сортировки
        faces_sorted = sorted(faces_slice, 
                            key=lambda x: float(np.mean(x[0][:, axis])))
        median_idx = len(faces_sorted) // 2
        
        # Создаем узел
        node = KDNode(faces_sorted[median_idx][0], 
                     faces_sorted[median_idx][1],
                     axis=axis)
        
        # Обновляем список лиц с отсортированными данными
        faces[start:end] = faces_sorted
        
        # Рекурсивно строим левое и правое поддерево
        mid = start + median_idx
        node.left = self._build_tree(faces, start, mid, 
                                   (axis + 1) % faces[0][0].shape[1])
        node.right = self._build_tree(faces, mid + 1, end,
                                    (axis + 1) % faces[0][0].shape[1])
        
        return node
        
    def build(self, faces: List[Tuple[np.ndarray, str]]) -> None:
        """Строит k-d дерево из списка лиц"""
        if not faces:
            return
            
        self.root = self._build_tree(faces, 0, len(faces), 0)
        self.size = len(faces)
        
    def _find_nearest(self, node: Optional[KDNode], 
                     target: np.ndarray,
                     best_dist: float = float('inf'),
                     best_node: Optional[KDNode] = None) -> Tuple[float, Optional[KDNode]]:
        """Рекурсивно находит ближайшее лицо"""
        if node is None:
            return best_dist, best_node
            
        # Вычисляем расстояние до текущего узла
        current_dist = float(np.mean(np.abs(node.face_data - target)))
        
        # Обновляем лучшее расстояние
        if current_dist < best_dist:
            best_dist = current_dist
            best_node = node
            
        # Определяем, в каком поддереве искать
        target_val = float(np.mean(target[:, node.axis]))
        node_val = float(np.mean(node.face_data[:, node.axis]))
        
        if target_val < node_val:
            first, second = node.left, node.right
        else:
            first, second = node.right, node.left
            
        # Рекурсивно ищем в первом поддереве
        best_dist, best_node = self._find_nearest(first, target, 
                                                best_dist, best_node)
        
        # Проверяем, нужно ли искать во втором поддереве
        axis_dist = abs(target_val - node_val)
        if axis_dist < best_dist:
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
            
        return best_node.user_id, float(np.mean(np.abs(best_node.face_data - target)))
        
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
                # Подсчитываем размер дерева
                def count_nodes(node: Optional[KDNode]) -> int:
                    if node is None:
                        return 0
                    return 1 + count_nodes(node.left) + count_nodes(node.right)
                self.size = count_nodes(self.root)
        except FileNotFoundError:
            self.root = None
            self.size = 0 