import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Настройка стиля
sns.set_theme()
plt.rcParams['font.family'] = 'DejaVu Sans'

# Загрузка данных
linear_data = pd.read_csv('results/benchmark_results.csv')
kd_tree_data = pd.read_csv('results/optimized_benchmark_results.csv')
enhanced_data = pd.read_csv('results/enhanced/benchmark_results.csv')

# Создание графика
plt.figure(figsize=(12, 8))

# Построение графиков для каждого алгоритма
# Линейный поиск
plt.plot(linear_data['database_size'], linear_data['avg_query_time'], 
         'b-', marker='o', linewidth=2, label='Линейный поиск')
plt.fill_between(linear_data['database_size'],
                linear_data['avg_query_time'] - linear_data['std_query_time'],
                linear_data['avg_query_time'] + linear_data['std_query_time'],
                alpha=0.2, color='blue')
plt.plot(linear_data['database_size'], linear_data['min_query_time'], 
         'g--', marker='^', label='Мин. время (лин.)')
plt.plot(linear_data['database_size'], linear_data['max_query_time'], 
         'r--', marker='v', label='Макс. время (лин.)')

# K-d дерево
plt.plot(kd_tree_data['database_size'], kd_tree_data['avg_query_time'], 
         'g-', marker='s', linewidth=2, label='K-d дерево')
plt.fill_between(kd_tree_data['database_size'],
                kd_tree_data['avg_query_time'] - kd_tree_data['std_query_time'],
                kd_tree_data['avg_query_time'] + kd_tree_data['std_query_time'],
                alpha=0.2, color='green')
plt.plot(kd_tree_data['database_size'], kd_tree_data['min_query_time'], 
         'g--', marker='^', label='Мин. время (k-d)')
plt.plot(kd_tree_data['database_size'], kd_tree_data['max_query_time'], 
         'r--', marker='v', label='Макс. время (k-d)')

# Улучшенный алгоритм
plt.plot(enhanced_data['database_size'], enhanced_data['avg_query_time'], 
         'r-', marker='d', linewidth=2, label='Улучшенный алгоритм')
plt.fill_between(enhanced_data['database_size'],
                enhanced_data['avg_query_time'] - enhanced_data['std_query_time'],
                enhanced_data['avg_query_time'] + enhanced_data['std_query_time'],
                alpha=0.2, color='red')
plt.plot(enhanced_data['database_size'], enhanced_data['min_query_time'], 
         'g--', marker='^', label='Мин. время (улучш.)')
plt.plot(enhanced_data['database_size'], enhanced_data['max_query_time'], 
         'r--', marker='v', label='Макс. время (улучш.)')

# Настройка графика
plt.title('Сравнение производительности алгоритмов поиска')
plt.xlabel('Размер базы данных (кол-во лиц)')
plt.ylabel('Время запроса (секунды)')
plt.grid(True)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

# Добавление статистики
stats_text = "Статистика по алгоритмам:\n\n"
stats_text += "Линейный поиск:\n"
stats_text += f"Среднее время: {linear_data['avg_query_time'].mean():.6f} ± {linear_data['std_query_time'].mean():.6f} сек\n"
stats_text += f"Мин. время: {linear_data['min_query_time'].min():.6f} сек\n"
stats_text += f"Макс. время: {linear_data['max_query_time'].max():.6f} сек\n\n"

stats_text += "K-d дерево:\n"
stats_text += f"Среднее время: {kd_tree_data['avg_query_time'].mean():.6f} ± {kd_tree_data['std_query_time'].mean():.6f} сек\n"
stats_text += f"Мин. время: {kd_tree_data['min_query_time'].min():.6f} сек\n"
stats_text += f"Макс. время: {kd_tree_data['max_query_time'].max():.6f} сек\n\n"

stats_text += "Улучшенный алгоритм:\n"
stats_text += f"Среднее время: {enhanced_data['avg_query_time'].mean():.6f} ± {enhanced_data['std_query_time'].mean():.6f} сек\n"
stats_text += f"Мин. время: {enhanced_data['min_query_time'].min():.6f} сек\n"
stats_text += f"Макс. время: {enhanced_data['max_query_time'].max():.6f} сек"

plt.figtext(0.02, 0.02, stats_text, fontsize=8, bbox=dict(facecolor='white', alpha=0.8))

# Сохранение графика
output_dir = Path('results/visualizations/comparison')
output_dir.mkdir(parents=True, exist_ok=True)
plt.savefig(output_dir / 'all_algorithms_comparison.png', dpi=300, bbox_inches='tight')
plt.close() 