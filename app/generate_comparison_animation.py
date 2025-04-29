import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import imageio
from matplotlib.gridspec import GridSpec
from matplotlib.animation import FuncAnimation
from matplotlib.ticker import FuncFormatter
import seaborn as sns
from typing import List, Dict

def format_time(x, pos):
    """Форматирование времени для оси Y"""
    if x >= 1:
        return f'{x:.1f} с'
    elif x >= 0.001:
        return f'{x*1000:.1f} мс'
    else:
        return f'{x*1000000:.1f} мкс'

def create_comparison_animation(basic_results: List[Dict], 
                              enhanced_results: List[Dict],
                              output_path: str = 'benchmark_animation.gif'):
    """
    Создает анимированное сравнение производительности алгоритмов
    
    Параметры:
    - basic_results: результаты базового алгоритма
    - enhanced_results: результаты улучшенного алгоритма
    - output_path: путь для сохранения анимации
    """
    # Создаем DataFrame из результатов
    df_basic = pd.DataFrame(basic_results)
    df_enhanced = pd.DataFrame(enhanced_results)
    
    # Настраиваем стиль графика
    plt.style.use('seaborn')
    sns.set_palette("husl")
    
    # Создаем фигуру
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), 
                                  gridspec_kw={'height_ratios': [2, 1]})
    
    # Настраиваем оси
    ax1.set_xlim(0, max(df_basic['database_size']) * 1.1)
    ax1.set_ylim(0, max(df_basic['avg_query_time']) * 1.2)
    ax2.set_xlim(0, max(df_basic['database_size']) * 1.1)
    ax2.set_ylim(0, 100)
    
    # Создаем пустые линии для анимации
    line1, = ax1.plot([], [], 'o-', label='Базовый алгоритм', linewidth=2)
    line2, = ax1.plot([], [], 's-', label='Улучшенный алгоритм', linewidth=2)
    bar = ax2.bar([], [], width=40, alpha=0.7, color='green')
    
    # Настраиваем графики
    ax1.set_xlabel('Размер базы данных', fontsize=12)
    ax1.set_ylabel('Время запроса', fontsize=12)
    ax1.set_title('Сравнение производительности алгоритмов', fontsize=14, pad=20)
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.legend(fontsize=10)
    ax1.yaxis.set_major_formatter(FuncFormatter(format_time))
    
    ax2.set_xlabel('Размер базы данных', fontsize=12)
    ax2.set_ylabel('Улучшение (%)', fontsize=12)
    ax2.set_title('Процент улучшения', fontsize=14, pad=20)
    ax2.grid(True, linestyle='--', alpha=0.7)
    
    # Функция инициализации анимации
    def init():
        line1.set_data([], [])
        line2.set_data([], [])
        for rect in bar:
            rect.set_height(0)
        return line1, line2, *bar
    
    # Функция обновления кадра
    def update(frame):
        # Обновляем первый график
        x_basic = df_basic['database_size'][:frame+1]
        y_basic = df_basic['avg_query_time'][:frame+1]
        x_enhanced = df_enhanced['database_size'][:frame+1]
        y_enhanced = df_enhanced['avg_query_time'][:frame+1]
        
        line1.set_data(x_basic, y_basic)
        line2.set_data(x_enhanced, y_enhanced)
        
        # Обновляем второй график
        improvement = ((df_basic['avg_query_time'][frame] - 
                       df_enhanced['avg_query_time'][frame]) / 
                      df_basic['avg_query_time'][frame] * 100)
        
        for rect in bar:
            rect.set_height(improvement)
            rect.set_x(df_basic['database_size'][frame] - 20)
        
        # Добавляем аннотации
        if frame == len(df_basic) - 1:
            for i, (x, y) in enumerate(zip(x_basic, y_basic)):
                ax1.annotate(f'{y*1000:.1f} мс', (x, y),
                           textcoords="offset points", xytext=(0,10), ha='center')
            for i, (x, y) in enumerate(zip(x_enhanced, y_enhanced)):
                ax1.annotate(f'{y*1000:.1f} мс', (x, y),
                           textcoords="offset points", xytext=(0,-15), ha='center')
            ax2.annotate(f'{improvement:.1f}%', 
                        (df_basic['database_size'][frame], improvement),
                        textcoords="offset points", xytext=(0,5), ha='center')
        
        return line1, line2, *bar
    
    # Создаем анимацию
    anim = FuncAnimation(fig, update, frames=len(df_basic),
                        init_func=init, blit=True, interval=500)
    
    # Сохраняем анимацию
    anim.save(output_path, writer='pillow', fps=2, dpi=100)
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
    
    # Генерируем анимацию
    create_comparison_animation(basic_results, enhanced_results, 'benchmark_animation.gif') 