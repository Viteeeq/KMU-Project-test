import os
import time
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple
from face_processor import FaceProcessor
import matplotlib.animation as animation

class Benchmark:
    def __init__(self, processor: FaceProcessor):
        self.processor = processor
        self.results = []
        self.intermediate_results = []
        
    def generate_test_data(self, num_users: int) -> None:
        """Генерирует тестовые данные для бенчмарка"""
        # Создаем директорию для тестовых данных
        if not os.path.exists('test_data'):
            os.makedirs('test_data')
            
        # Генерируем тестовые изображения лиц
        for i in range(num_users):
            if not os.path.exists(f'test_data/face_{i}.jpg'):
                # Создаем случайное изображение лица
                face = np.random.randint(0, 255, (100, 100), dtype=np.uint8)
                # Добавляем случайный шум
                noise = np.random.normal(0, 10, (100, 100)).astype(np.uint8)
                face = cv2.add(face, noise)
                # Сохраняем изображение
                cv2.imwrite(f'test_data/face_{i}.jpg', face)
            
    def run_benchmark(self, database_sizes: List[int], num_queries: int) -> pd.DataFrame:
        """Запускает тестирование производительности"""
        results = []
        self.intermediate_results = []
        
        for size in database_sizes:
            print(f"Тестирование с размером базы данных: {size}")
            
            # Очищаем предыдущие данные
            self.processor.clear_database()
            
            # Добавляем тестовые данные в базу
            for i in range(size):
                face = cv2.imread(f'test_data/face_{i}.jpg', cv2.IMREAD_GRAYSCALE)
                self.processor.add_face(face, f"user_{i}")
                
            # Измеряем время запросов
            query_times = []
            for q in range(num_queries):
                # Выбираем случайное лицо для запроса
                query_idx = np.random.randint(0, size)
                query_face = cv2.imread(f'test_data/face_{query_idx}.jpg', cv2.IMREAD_GRAYSCALE)
                
                # Измеряем время распознавания
                start_time = time.time()
                self.processor.recognize_face(query_face)
                end_time = time.time()
                
                query_time = end_time - start_time
                query_times.append(query_time)
                
                # Сохраняем промежуточные результаты для анимации
                if q % 10 == 0:  # Сохраняем каждый 10-й результат
                    self.intermediate_results.append({
                        'database_size': size,
                        'query_number': q,
                        'query_time': query_time
                    })
                
            # Сохраняем результаты
            results.append({
                'database_size': size,
                'avg_query_time': np.mean(query_times),
                'std_query_time': np.std(query_times),
                'min_query_time': np.min(query_times),
                'max_query_time': np.max(query_times)
            })
            
        return pd.DataFrame(results)
        
    def plot_results(self, results: pd.DataFrame, save_path: str) -> None:
        """Строит график результатов тестирования"""
        plt.figure(figsize=(12, 8))
        
        # Создаем основной график
        ax1 = plt.subplot(111)
        
        # Строим график среднего времени запроса
        line = ax1.plot(results['database_size'], results['avg_query_time'], 
                marker='o', label='Среднее время', linewidth=2, markersize=8)
                
        # Добавляем доверительные интервалы
        ax1.fill_between(results['database_size'],
                        results['avg_query_time'] - results['std_query_time'],
                        results['avg_query_time'] + results['std_query_time'],
                        alpha=0.2, label='Доверительный интервал')
                        
        # Добавляем точки минимального и максимального времени
        ax1.scatter(results['database_size'], results['min_query_time'], 
                   color='green', marker='^', label='Минимальное время', s=100)
        ax1.scatter(results['database_size'], results['max_query_time'], 
                   color='red', marker='v', label='Максимальное время', s=100)
        
        # Настраиваем оси и заголовки
        ax1.set_xlabel('Размер базы данных (количество лиц)', fontsize=12)
        ax1.set_ylabel('Время запроса (секунды)', fontsize=12)
        ax1.set_title('Производительность системы распознавания лиц', 
                     fontsize=14, pad=20)
        
        # Добавляем сетку
        ax1.grid(True, linestyle='--', alpha=0.7)
        
        # Добавляем легенду
        ax1.legend(loc='upper left', fontsize=10)
        
        # Добавляем аннотации с точными значениями
        for i, row in results.iterrows():
            ax1.annotate(f'{row["avg_query_time"]:.3f}с',
                        (row['database_size'], row['avg_query_time']),
                        xytext=(10, 10), textcoords='offset points')
        
        # Добавляем текстовую информацию о производительности
        perf_text = (
            f"Анализ производительности:\n"
            f"• Среднее время запроса растет линейно\n"
            f"• При 1000 лицах: {results.iloc[-1]['avg_query_time']:.3f}с\n"
            f"• Стандартное отклонение: {results.iloc[-1]['std_query_time']:.3f}с"
        )
        plt.figtext(0.02, 0.02, perf_text, fontsize=10, 
                   bbox=dict(facecolor='white', alpha=0.8))
        
        # Настраиваем стиль графика
        plt.style.use('default')
        
        # Сохраняем график с высоким разрешением
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
    def create_animation(self, save_path: str) -> None:
        """Создает анимированный график процесса тестирования"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        def update(frame):
            ax.clear()
            current_data = pd.DataFrame(self.intermediate_results[:frame])
            
            if not current_data.empty:
                # Получаем уникальные размеры базы данных
                sizes = current_data['database_size'].unique()
                
                # Создаем цветовую карту для разных размеров
                colors = plt.cm.viridis(np.linspace(0, 1, len(sizes)))
                
                for idx, size in enumerate(sizes):
                    size_data = current_data[current_data['database_size'] == size]
                    
                    # Строим график рассеяния для каждого размера
                    scatter = ax.scatter(size_data['query_number'], 
                                       size_data['query_time'],
                                       c=[colors[idx]], 
                                       label=f'БД размером {size}',
                                       alpha=0.6,
                                       s=100)
                    
                    # Добавляем линию тренда
                    if len(size_data) > 1:
                        z = np.polyfit(size_data['query_number'], 
                                     size_data['query_time'], 1)
                        p = np.poly1d(z)
                        ax.plot(size_data['query_number'], 
                               p(size_data['query_number']),
                               c=colors[idx], 
                               alpha=0.3,
                               linestyle='--')
                
                # Настраиваем график
                ax.set_xlabel('Номер запроса', fontsize=12)
                ax.set_ylabel('Время запроса (секунды)', fontsize=12)
                ax.set_title('Процесс тестирования производительности', 
                           fontsize=14, pad=20)
                ax.grid(True, linestyle='--', alpha=0.7)
                ax.legend(loc='upper left', fontsize=10)
                
                # Добавляем информацию о текущем прогрессе
                progress = frame / len(self.intermediate_results) * 100
                ax.text(0.02, 0.98, f'Прогресс: {progress:.1f}%',
                       transform=ax.transAxes,
                       fontsize=10,
                       verticalalignment='top',
                       bbox=dict(facecolor='white', alpha=0.8))
                
                # Добавляем статистику
                if len(current_data) > 0:
                    stats_text = (
                        f"Статистика:\n"
                        f"• Среднее время: {current_data['query_time'].mean():.3f}с\n"
                        f"• Максимальное время: {current_data['query_time'].max():.3f}с\n"
                        f"• Минимальное время: {current_data['query_time'].min():.3f}с"
                    )
                    ax.text(0.02, 0.02, stats_text,
                           transform=ax.transAxes,
                           fontsize=10,
                           bbox=dict(facecolor='white', alpha=0.8))
        
        # Создаем анимацию
        anim = animation.FuncAnimation(fig, update, 
                                     frames=len(self.intermediate_results),
                                     interval=50,  # 50ms между кадрами
                                     repeat=False)
        
        # Сохраняем анимацию
        anim.save(save_path, writer='pillow', fps=20)
        plt.close()
        
    def create_slow_animation(self, save_path: str) -> None:
        """Создает медленную версию анимированного графика процесса тестирования"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        def update(frame):
            ax.clear()
            current_data = pd.DataFrame(self.intermediate_results[:frame])
            
            if not current_data.empty:
                # Получаем уникальные размеры базы данных
                sizes = current_data['database_size'].unique()
                
                # Создаем цветовую карту для разных размеров
                colors = plt.cm.viridis(np.linspace(0, 1, len(sizes)))
                
                for idx, size in enumerate(sizes):
                    size_data = current_data[current_data['database_size'] == size]
                    
                    # Строим график рассеяния для каждого размера
                    scatter = ax.scatter(size_data['query_number'], 
                                       size_data['query_time'],
                                       c=[colors[idx]], 
                                       label=f'БД размером {size}',
                                       alpha=0.6,
                                       s=100)
                    
                    # Добавляем линию тренда
                    if len(size_data) > 1:
                        z = np.polyfit(size_data['query_number'], 
                                     size_data['query_time'], 1)
                        p = np.poly1d(z)
                        ax.plot(size_data['query_number'], 
                               p(size_data['query_number']),
                               c=colors[idx], 
                               alpha=0.5,
                               linewidth=3,
                               linestyle='--')
                
                # Настраиваем график
                ax.set_xlabel('Номер запроса', fontsize=12)
                ax.set_ylabel('Время запроса (секунды)', fontsize=12)
                ax.set_title('Процесс тестирования производительности (медленная версия)', 
                           fontsize=14, pad=20)
                ax.grid(True, linestyle='--', alpha=0.7)
                ax.legend(loc='upper left', fontsize=10)
                
                # Добавляем информацию о текущем прогрессе
                progress = frame / len(self.intermediate_results) * 100
                ax.text(0.02, 0.98, f'Прогресс: {progress:.1f}%',
                       transform=ax.transAxes,
                       fontsize=10,
                       verticalalignment='top',
                       bbox=dict(facecolor='white', alpha=0.8))
                
                # Добавляем статистику
                if len(current_data) > 0:
                    stats_text = (
                        f"Статистика:\n"
                        f"• Среднее время: {current_data['query_time'].mean():.3f}с\n"
                        f"• Максимальное время: {current_data['query_time'].max():.3f}с\n"
                        f"• Минимальное время: {current_data['query_time'].min():.3f}с"
                    )
                    ax.text(0.02, 0.02, stats_text,
                           transform=ax.transAxes,
                           fontsize=10,
                           bbox=dict(facecolor='white', alpha=0.8))
        
        # Создаем анимацию с более медленным обновлением
        anim = animation.FuncAnimation(fig, update, 
                                     frames=len(self.intermediate_results),
                                     interval=100,  # 100ms между кадрами
                                     repeat=False)
        
        # Сохраняем анимацию
        anim.save(save_path, writer='pillow', fps=10)  # Уменьшаем FPS до 10
        plt.close()
        
    def save_results(self, results: pd.DataFrame, save_path: str) -> None:
        """Сохраняет результаты в CSV файл"""
        results.to_csv(save_path, index=False)

if __name__ == "__main__":
    # Инициализация
    processor = FaceProcessor()
    benchmark = Benchmark(processor)
    
    # Запуск тестирования
    database_sizes = [10, 50, 100, 250, 500, 1000]
    results = benchmark.run_benchmark(database_sizes, 100)
    
    # Сохранение и визуализация результатов
    benchmark.save_results(results, 'benchmark_results.csv')
    benchmark.plot_results(results, 'benchmark_results.png')
    benchmark.create_animation('benchmark_animation.gif')
    benchmark.create_slow_animation('benchmark_animation_slow.gif') 