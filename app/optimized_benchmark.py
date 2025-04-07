import time
import pandas as pd
import numpy as np
from typing import List, Dict
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from app.optimized_face_processor import OptimizedFaceProcessor
from app.data_generator import DataGenerator

class OptimizedBenchmark:
    def __init__(self, processor: OptimizedFaceProcessor):
        """Инициализация бенчмарка"""
        self.processor = processor
        self.intermediate_results = []
        
    def run_benchmark(self, database_sizes: List[int], 
                     num_queries: int) -> pd.DataFrame:
        """Запускает тестирование производительности"""
        results = []
        
        for size in database_sizes:
            print(f"Тестирование с размером базы данных: {size}")
            
            # Генерируем тестовые данные
            generator = DataGenerator()
            faces = generator.generate_faces(size)
            
            # Очищаем базу данных
            self.processor.db.clear_database()
            
            # Добавляем лица в базу
            for i, face in enumerate(faces):
                self.processor.add_face(face, f"user_{i}")
            
            # Тестируем поиск
            query_times = []
            for i in range(num_queries):
                # Генерируем тестовое лицо
                test_face = generator.generate_face()
                
                # Измеряем время поиска
                start_time = time.time()
                user_id, distance = self.processor.recognize_face(test_face)
                end_time = time.time()
                
                query_time = end_time - start_time
                query_times.append(query_time)
                
                # Сохраняем промежуточный результат
                self.intermediate_results.append({
                    'database_size': size,
                    'query_number': i,
                    'query_time': query_time
                })
            
            # Вычисляем статистику
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
        ax1.set_title('Производительность системы распознавания лиц (k-d дерево)', 
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
            f"• Среднее время запроса растет логарифмически\n"
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
                               alpha=0.5,
                               linewidth=3,
                               linestyle='--')
                
                # Настраиваем график
                ax.set_xlabel('Номер запроса', fontsize=12)
                ax.set_ylabel('Время запроса (секунды)', fontsize=12)
                ax.set_title('Процесс тестирования производительности (k-d дерево)', 
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