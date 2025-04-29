import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np

# Настройка стиля графиков
sns.set_theme()
plt.rcParams['font.family'] = 'DejaVu Sans'

def create_benchmark_plots(data, algorithm_name):
    plt.figure(figsize=(12, 8))
    
    # Основная линия - среднее время запроса
    plt.plot(data['database_size'], data['avg_query_time'], 
             marker='o', linewidth=2, label='Среднее время')
    
    # Доверительный интервал
    plt.fill_between(data['database_size'],
                    data['avg_query_time'] - data['std_query_time'],
                    data['avg_query_time'] + data['std_query_time'],
                    alpha=0.2, label='Доверительный интервал')
    
    # Минимальное и максимальное время
    plt.plot(data['database_size'], data['min_query_time'], 
             'g--', marker='^', label='Минимальное время')
    plt.plot(data['database_size'], data['max_query_time'], 
             'r--', marker='v', label='Максимальное время')
    
    # Настройка графика
    plt.title(f'Тест производительности: {algorithm_name}')
    plt.xlabel('Размер базы данных (кол-во лиц)')
    plt.ylabel('Время (секунды)')
    plt.grid(True)
    plt.legend(loc='upper left')
    
    # Добавление статистики
    stats_text = f"Статистика:\n" \
                f"Среднее время: {data['avg_query_time'].mean():.6f} ± {data['std_query_time'].mean():.6f} сек\n" \
                f"Минимальное время: {data['min_query_time'].min():.6f} сек\n" \
                f"Максимальное время: {data['max_query_time'].max():.6f} сек"
    if 'memory_usage_mb' in data.columns:
        stats_text += f'\nСреднее использование памяти: {data["memory_usage_mb"].mean():.1f} МБ'
    
    plt.figtext(0.02, 0.02, stats_text, fontsize=8, bbox=dict(facecolor='white', alpha=0.8))
    
    # Сохранение графика
    output_dir = Path('results/visualizations')
    if algorithm_name == 'Базовый поиск':
        output_dir = output_dir / 'linear'
    elif algorithm_name == 'K-d дерево':
        output_dir = output_dir / 'kd_tree'
    else:
        output_dir = output_dir / 'enhanced'
    
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_dir / 'performance.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    # Загрузка данных для базового алгоритма
    linear_data = pd.read_csv('results/benchmark_results.csv')
    create_benchmark_plots(linear_data, 'Базовый поиск')
    
    # Загрузка данных для k-d дерева
    kd_tree_data = pd.read_csv('results/optimized_benchmark_results.csv')
    create_benchmark_plots(kd_tree_data, 'K-d дерево')
    
    # Загрузка данных для улучшенного алгоритма
    enhanced_data = pd.read_csv('results/enhanced/benchmark_results.csv')
    create_benchmark_plots(enhanced_data, 'Улучшенный алгоритм')
    
    print("Все визуализации успешно созданы и сохранены в папке results/visualizations")

if __name__ == "__main__":
    main() 