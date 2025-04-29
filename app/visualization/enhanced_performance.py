import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from pathlib import Path

# Настройка стиля графиков
sns.set_theme()
plt.rcParams['font.family'] = 'DejaVu Sans'

# Загружаем данные
enhanced_data = pd.read_csv('../../results/enhanced/benchmark_results.csv')

# Создаем директории для результатов
output_dir = Path('../../results/visualizations/enhanced/benchmarks')
output_dir.mkdir(parents=True, exist_ok=True)

# График времени запроса
plt.figure(figsize=(12, 8))

# Основная линия со средним временем
plt.plot(enhanced_data['database_size'], enhanced_data['avg_query_time'], 
         marker='o', linewidth=2, label='Среднее время')

# Доверительный интервал
plt.fill_between(enhanced_data['database_size'],
                 enhanced_data['avg_query_time'] - enhanced_data['std_query_time'],
                 enhanced_data['avg_query_time'] + enhanced_data['std_query_time'],
                 alpha=0.2, label='Доверительный интервал')

# Минимальное и максимальное время
plt.plot(enhanced_data['database_size'], enhanced_data['min_query_time'], 
         'g--', marker='^', label='Минимальное время')
plt.plot(enhanced_data['database_size'], enhanced_data['max_query_time'], 
         'r--', marker='v', label='Максимальное время')

# Добавляем статистику в сноску
stats_text = f"Статистика:\n" \
            f"Среднее время: {enhanced_data['avg_query_time'].mean():.6f} ± {enhanced_data['std_query_time'].mean():.6f} сек\n" \
            f"Минимальное время: {enhanced_data['min_query_time'].min():.6f} сек\n" \
            f"Максимальное время: {enhanced_data['max_query_time'].max():.6f} сек"

plt.figtext(0.02, 0.02, stats_text, fontsize=8, bbox=dict(facecolor='white', alpha=0.8))

plt.title('Тест производительности алгоритма с биометрическими признаками')
plt.xlabel('Размер базы данных (кол-во лиц)')
plt.ylabel('Время (секунды)')
plt.grid(True)
plt.legend(loc='upper left')
plt.savefig(output_dir / 'query_time.png', dpi=300, bbox_inches='tight')
plt.close() 