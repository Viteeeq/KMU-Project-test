import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Настройка стиля
sns.set_theme()
plt.rcParams['font.family'] = 'DejaVu Sans'

# Загрузка данных
kd_tree_data = pd.read_csv('results/optimized_benchmark_results.csv')
enhanced_data = pd.read_csv('results/enhanced/benchmark_results.csv')

# Создание графика
plt.figure(figsize=(12, 8))

# Построение графиков для каждого алгоритма
# K-d дерево (зеленые оттенки)
plt.plot(kd_tree_data['database_size'], kd_tree_data['avg_query_time'], 
         '#2E8B57', marker='s', linewidth=2, label='K-d дерево (среднее)')
plt.fill_between(kd_tree_data['database_size'],
                kd_tree_data['avg_query_time'] - kd_tree_data['std_query_time'],
                kd_tree_data['avg_query_time'] + kd_tree_data['std_query_time'],
                alpha=0.2, color='#2E8B57')
plt.plot(kd_tree_data['database_size'], kd_tree_data['min_query_time'], 
         '#90EE90', marker='^', label='K-d дерево (мин.)')
plt.plot(kd_tree_data['database_size'], kd_tree_data['max_query_time'], 
         '#006400', marker='v', label='K-d дерево (макс.)')

# Улучшенный алгоритм (синие оттенки)
plt.plot(enhanced_data['database_size'], enhanced_data['avg_query_time'], 
         '#1E90FF', marker='d', linewidth=2, label='Улучшенный (среднее)')
plt.fill_between(enhanced_data['database_size'],
                enhanced_data['avg_query_time'] - enhanced_data['std_query_time'],
                enhanced_data['avg_query_time'] + enhanced_data['std_query_time'],
                alpha=0.2, color='#1E90FF')
plt.plot(enhanced_data['database_size'], enhanced_data['min_query_time'], 
         '#87CEEB', marker='^', label='Улучшенный (мин.)')
plt.plot(enhanced_data['database_size'], enhanced_data['max_query_time'], 
         '#00008B', marker='v', label='Улучшенный (макс.)')

# Настройка графика
plt.title('Сравнение производительности оптимизированных алгоритмов поиска')
plt.xlabel('Размер базы данных (кол-во лиц)')
plt.ylabel('Время запроса (секунды)')
plt.grid(True)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

# Добавление статистики
stats_text = "Статистика по алгоритмам:\n\n"
stats_text += "K-d дерево:\n"
stats_text += f"Среднее время: {kd_tree_data['avg_query_time'].mean():.6f} ± {kd_tree_data['std_query_time'].mean():.6f} сек\n"
stats_text += f"Мин. время: {kd_tree_data['min_query_time'].min():.6f} сек\n"
stats_text += f"Макс. время: {kd_tree_data['max_query_time'].max():.6f} сек\n\n"

stats_text += "Улучшенный алгоритм:\n"
stats_text += f"Среднее время: {enhanced_data['avg_query_time'].mean():.6f} ± {enhanced_data['std_query_time'].mean():.6f} сек\n"
stats_text += f"Мин. время: {enhanced_data['min_query_time'].min():.6f} сек\n"
stats_text += f"Макс. время: {enhanced_data['max_query_time'].max():.6f} сек\n\n"

# Добавление сравнения производительности
speedup = enhanced_data['avg_query_time'].mean() / kd_tree_data['avg_query_time'].mean()
stats_text += f"K-d дерево быстрее улучшенного алгоритма в {speedup:.2f} раз"

plt.figtext(0.02, 0.02, stats_text, fontsize=8, bbox=dict(facecolor='white', alpha=0.8))

# Сохранение графика
output_dir = Path('results/visualizations/comparison')
output_dir.mkdir(parents=True, exist_ok=True)
plt.savefig(output_dir / 'optimized_algorithms_comparison.png', dpi=300, bbox_inches='tight')
plt.close() 