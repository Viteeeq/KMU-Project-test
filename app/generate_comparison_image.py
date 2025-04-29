import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict
import seaborn as sns
from matplotlib.ticker import FuncFormatter

def format_time(x, pos):
    """Форматирование времени для оси Y"""
    if x >= 1:
        return f'{x:.1f} с'
    elif x >= 0.001:
        return f'{x*1000:.1f} мс'
    else:
        return f'{x*1000000:.1f} мкс'

def plot_comparison(results: List[Dict], output_path: str = 'benchmark_results.png'):
    """
    Создает график сравнения производительности алгоритмов
    
    Параметры:
    - results: список словарей с результатами тестирования
    - output_path: путь для сохранения графика
    """
    # Создаем DataFrame из результатов
    df = pd.DataFrame(results)
    
    # Настраиваем стиль графика
    plt.style.use('seaborn')
    sns.set_palette("husl")
    
    # Создаем фигуру с двумя подграфиками
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [2, 1]})
    
    # Первый график: время запроса
    ax1.plot(df['database_size'], df['avg_query_time'], 
             marker='o', linewidth=2, label='Среднее время запроса')
    ax1.fill_between(df['database_size'], 
                    df['avg_query_time'] - df['std_query_time'],
                    df['avg_query_time'] + df['std_query_time'],
                    alpha=0.2)
    
    # Добавляем теоретическую линию O(log n)
    theoretical_log = df['avg_query_time'].iloc[0] * np.log2(df['database_size'] / df['database_size'].iloc[0])
    ax1.plot(df['database_size'], theoretical_log, '--', 
             label='Теоретическая O(log n)', alpha=0.7)
    
    # Настраиваем первый график
    ax1.set_xlabel('Размер базы данных', fontsize=12)
    ax1.set_ylabel('Время запроса', fontsize=12)
    ax1.set_title('Производительность алгоритма поиска', fontsize=14, pad=20)
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.legend(fontsize=10)
    ax1.yaxis.set_major_formatter(FuncFormatter(format_time))
    
    # Второй график: процент улучшения
    ax2.bar(df['database_size'], df['improvement_percent'], 
            width=40, alpha=0.7, color='green')
    
    # Настраиваем второй график
    ax2.set_xlabel('Размер базы данных', fontsize=12)
    ax2.set_ylabel('Улучшение (%)', fontsize=12)
    ax2.set_title('Процент улучшения по сравнению с линейным поиском', 
                 fontsize=14, pad=20)
    ax2.grid(True, linestyle='--', alpha=0.7)
    
    # Добавляем аннотации с точными значениями
    for i, row in df.iterrows():
        ax1.annotate(f'{row["avg_query_time"]*1000:.1f} мс', 
                    (row['database_size'], row['avg_query_time']),
                    textcoords="offset points", xytext=(0,10), ha='center')
        ax2.annotate(f'{row["improvement_percent"]:.1f}%', 
                    (row['database_size'], row['improvement_percent']),
                    textcoords="offset points", xytext=(0,5), ha='center')
    
    # Настраиваем общий вид
    plt.tight_layout()
    
    # Сохраняем график
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def plot_algorithm_comparison(basic_results: List[Dict], 
                            enhanced_results: List[Dict],
                            output_path: str = 'algorithm_comparison.png'):
    """
    Создает график сравнения базового и улучшенного алгоритмов
    
    Параметры:
    - basic_results: результаты базового алгоритма
    - enhanced_results: результаты улучшенного алгоритма
    - output_path: путь для сохранения графика
    """
    # Создаем DataFrame из результатов
    df_basic = pd.DataFrame(basic_results)
    df_enhanced = pd.DataFrame(enhanced_results)
    
    # Настраиваем стиль графика
    plt.style.use('seaborn')
    sns.set_palette("husl")
    
    # Создаем фигуру
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Строим графики для обоих алгоритмов
    ax.plot(df_basic['database_size'], df_basic['avg_query_time'], 
            marker='o', linewidth=2, label='Базовый алгоритм')
    ax.plot(df_enhanced['database_size'], df_enhanced['avg_query_time'], 
            marker='s', linewidth=2, label='Улучшенный алгоритм')
    
    # Добавляем области неопределенности
    ax.fill_between(df_basic['database_size'], 
                   df_basic['avg_query_time'] - df_basic['std_query_time'],
                   df_basic['avg_query_time'] + df_basic['std_query_time'],
                   alpha=0.2)
    ax.fill_between(df_enhanced['database_size'], 
                   df_enhanced['avg_query_time'] - df_enhanced['std_query_time'],
                   df_enhanced['avg_query_time'] + df_enhanced['std_query_time'],
                   alpha=0.2)
    
    # Настраиваем график
    ax.set_xlabel('Размер базы данных', fontsize=12)
    ax.set_ylabel('Время запроса', fontsize=12)
    ax.set_title('Сравнение производительности алгоритмов', fontsize=14, pad=20)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(fontsize=10)
    ax.yaxis.set_major_formatter(FuncFormatter(format_time))
    
    # Добавляем аннотации с точными значениями
    for df, marker in [(df_basic, 'o'), (df_enhanced, 's')]:
        for _, row in df.iterrows():
            ax.annotate(f'{row["avg_query_time"]*1000:.1f} мс', 
                       (row['database_size'], row['avg_query_time']),
                       textcoords="offset points", 
                       xytext=(0,10 if marker == 'o' else -15), 
                       ha='center')
    
    # Настраиваем общий вид
    plt.tight_layout()
    
    # Сохраняем график
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    # Пример использования
    basic_results = [
        {'database_size': 10, 'avg_query_time': 0.005, 'std_query_time': 0.001},
        {'database_size': 50, 'avg_query_time': 0.025, 'std_query_time': 0.002},
        {'database_size': 100, 'avg_query_time': 0.05, 'std_query_time': 0.003},
        {'database_size': 250, 'avg_query_time': 0.125, 'std_query_time': 0.005},
        {'database_size': 500, 'avg_query_time': 0.25, 'std_query_time': 0.008},
        {'database_size': 1000, 'avg_query_time': 0.5, 'std_query_time': 0.01}
    ]
    
    enhanced_results = [
        {'database_size': 10, 'avg_query_time': 0.0009114, 'std_query_time': 0.0001235},
        {'database_size': 50, 'avg_query_time': 0.0008425, 'std_query_time': 0.0001338},
        {'database_size': 100, 'avg_query_time': 0.0009224, 'std_query_time': 0.0001093},
        {'database_size': 250, 'avg_query_time': 0.0006318, 'std_query_time': 0.0000839},
        {'database_size': 500, 'avg_query_time': 0.0007624, 'std_query_time': 0.0001764},
        {'database_size': 1000, 'avg_query_time': 0.0006820, 'std_query_time': 0.0000982}
    ]
    
    # Генерируем графики
    plot_comparison(enhanced_results, 'benchmark_results.png')
    plot_algorithm_comparison(basic_results, enhanced_results, 'algorithm_comparison.png') 