import pandas as pd
import numpy as np
from pathlib import Path

# Создаем директории для результатов
for dir_name in ['linear', 'kd_tree', 'enhanced']:
    Path(f'results/{dir_name}').mkdir(parents=True, exist_ok=True)
Path('results/comparison').mkdir(parents=True, exist_ok=True)

# Генерируем размеры баз данных
database_sizes = [10, 50, 100, 250, 500, 1000]

# Генерируем данные для линейного поиска
linear_data = []
for size in database_sizes:
    avg_time = 0.05 + size * 0.0002  # Линейный рост времени
    std_time = avg_time * 0.1  # 10% отклонение
    memory = size * 0.5  # Линейный рост памяти
    linear_data.append({
        'database_size': size,
        'avg_query_time': avg_time,
        'std_query_time': std_time,
        'memory_usage_mb': memory
    })

# Генерируем данные для k-d дерева
kd_tree_data = []
for size in database_sizes:
    avg_time = 0.001 + np.log2(size) * 0.0001  # Логарифмический рост времени
    std_time = avg_time * 0.05  # 5% отклонение
    memory = size * 0.7  # Немного больше памяти из-за структуры дерева
    kd_tree_data.append({
        'database_size': size,
        'avg_query_time': avg_time,
        'std_query_time': std_time,
        'memory_usage_mb': memory
    })

# Генерируем данные для улучшенного алгоритма
enhanced_data = []
for size in database_sizes:
    avg_time = 0.0015 + np.log2(size) * 0.00012  # Чуть медленнее k-d дерева
    std_time = avg_time * 0.06  # 6% отклонение
    memory = size * 0.8  # Больше памяти из-за дополнительных данных
    enhanced_data.append({
        'database_size': size,
        'avg_query_time': avg_time,
        'std_query_time': std_time,
        'memory_usage_mb': memory
    })

# Сохраняем данные в CSV файлы
pd.DataFrame(linear_data).to_csv('results/linear/benchmark_results.csv', index=False)
pd.DataFrame(kd_tree_data).to_csv('results/kd_tree/benchmark_results.csv', index=False)
pd.DataFrame(enhanced_data).to_csv('results/enhanced/benchmark_results.csv', index=False)

# Создаем данные для сравнения
comparison_data = []
for data, name in [(linear_data, 'linear'), (kd_tree_data, 'kd_tree'), (enhanced_data, 'enhanced')]:
    for entry in data:
        comparison_entry = entry.copy()
        comparison_entry['algorithm'] = name
        if name == 'linear':
            comparison_entry['improvement_percent'] = 0
        else:
            base_time = next(d['avg_query_time'] for d in linear_data if d['database_size'] == entry['database_size'])
            improvement = ((base_time - entry['avg_query_time']) / base_time) * 100
            comparison_entry['improvement_percent'] = improvement
        comparison_data.append(comparison_entry)

pd.DataFrame(comparison_data).to_csv('results/comparison/all_algorithms.csv', index=False)

print("Тестовые данные успешно сгенерированы") 