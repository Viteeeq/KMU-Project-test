import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Загружаем данные
linear_data = pd.read_csv('../../results/linear/benchmark_results.csv')
kdtree_data = pd.read_csv('../../results/kd_tree/benchmark_results.csv')
enhanced_data = pd.read_csv('../../results/enhanced/benchmark_results.csv')

# Устанавливаем стиль
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Создаем график
plt.figure(figsize=(10, 6))

# Функция для построения графика с доверительным интервалом
def plot_algorithm(data, label, color):
    plt.plot(data['database_size'], data['avg_query_time'], 
             marker='o', linewidth=2, label=label, color=color)
    plt.fill_between(data['database_size'],
                     data['avg_query_time'] - data['std_query_time'],
                     data['avg_query_time'] + data['std_query_time'],
                     alpha=0.2, color=color)

# Рисуем графики для каждого алгоритма
plot_algorithm(linear_data, 'Linear Search', 'blue')
plot_algorithm(kdtree_data, 'K-d Tree', 'green')
plot_algorithm(enhanced_data, 'Enhanced Algorithm', 'red')

# Настраиваем оси и заголовок
plt.xlabel('Размер базы данных (кол-во лиц)', fontsize=12)
plt.ylabel('Время запроса (секунды)', fontsize=12)
plt.title('Сравнение производительности алгоритмов', fontsize=14, pad=20)

# Добавляем сетку
plt.grid(True, linestyle='--', alpha=0.7)

# Добавляем легенду
plt.legend(fontsize=10, loc='upper left')

# Добавляем статистику в виде текста
stats_text = f"""
Статистика:
Linear Search:
- Среднее время: {linear_data['avg_query_time'].mean():.6f} ± {linear_data['std_query_time'].mean():.6f} сек
- Использование памяти: {linear_data['memory_usage_mb'].max():.1f} МБ

K-d Tree:
- Среднее время: {kdtree_data['avg_query_time'].mean():.6f} ± {kdtree_data['std_query_time'].mean():.6f} сек
- Использование памяти: {kdtree_data['memory_usage_mb'].max():.1f} МБ

Enhanced Algorithm:
- Среднее время: {enhanced_data['avg_query_time'].mean():.6f} ± {enhanced_data['std_query_time'].mean():.6f} сек
- Минимальное время: {enhanced_data['min_query_time'].min():.6f} сек
- Максимальное время: {enhanced_data['max_query_time'].max():.6f} сек
"""
plt.figtext(0.15, 0.02, stats_text, fontsize=10, bbox=dict(facecolor='white', alpha=0.8))

# Настраиваем отступы
plt.tight_layout()

# Создаем директорию для результатов, если она не существует
os.makedirs('../../results/visualizations', exist_ok=True)

# Сохраняем график
plt.savefig('../../results/visualizations/performance_comparison.png', dpi=300, bbox_inches='tight')
plt.close() 