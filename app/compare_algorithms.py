import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def load_results():
    """Загружает результаты тестирования обоих алгоритмов"""
    linear = pd.read_csv('benchmark_results.csv')
    optimized = pd.read_csv('results/optimized_benchmark_results.csv')
    return linear, optimized

def plot_comparison(linear: pd.DataFrame, optimized: pd.DataFrame, save_path: str):
    """Строит сравнительный график производительности"""
    plt.figure(figsize=(15, 10))
    
    # Создаем основной график
    ax1 = plt.subplot(111)
    
    # Строим графики среднего времени запроса
    ax1.plot(linear['database_size'], linear['avg_query_time'], 
             marker='o', label='Линейный поиск', linewidth=2, 
             markersize=8, color='#FF6B6B')
    ax1.plot(optimized['database_size'], optimized['avg_query_time'], 
             marker='s', label='k-d дерево', linewidth=2, 
             markersize=8, color='#4ECDC4')
    
    # Добавляем доверительные интервалы
    ax1.fill_between(linear['database_size'],
                    linear['avg_query_time'] - linear['std_query_time'],
                    linear['avg_query_time'] + linear['std_query_time'],
                    alpha=0.2, color='#FF6B6B')
    ax1.fill_between(optimized['database_size'],
                    optimized['avg_query_time'] - optimized['std_query_time'],
                    optimized['avg_query_time'] + optimized['std_query_time'],
                    alpha=0.2, color='#4ECDC4')
    
    # Настраиваем оси и заголовки
    ax1.set_xlabel('Размер базы данных (количество лиц)', fontsize=12)
    ax1.set_ylabel('Время запроса (секунды)', fontsize=12)
    ax1.set_title('Сравнение производительности алгоритмов', 
                 fontsize=14, pad=20)
    
    # Добавляем сетку
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # Добавляем легенду
    ax1.legend(loc='upper left', fontsize=10)
    
    # Добавляем аннотации с точными значениями
    for i, row in linear.iterrows():
        ax1.annotate(f'{row["avg_query_time"]:.3f}с',
                    (row['database_size'], row['avg_query_time']),
                    xytext=(10, 10), textcoords='offset points',
                    color='#FF6B6B')
    for i, row in optimized.iterrows():
        ax1.annotate(f'{row["avg_query_time"]:.3f}с',
                    (row['database_size'], row['avg_query_time']),
                    xytext=(10, -15), textcoords='offset points',
                    color='#4ECDC4')
    
    # Вычисляем улучшение производительности
    improvement = ((linear['avg_query_time'] - optimized['avg_query_time']) / 
                  linear['avg_query_time'] * 100)
    
    # Добавляем текстовую информацию о производительности
    stats_text = (
        f"Анализ производительности:\n"
        f"Линейный поиск:\n"
        f"• При 1000 лицах: {linear.iloc[-1]['avg_query_time']:.3f}с\n"
        f"• Стандартное отклонение: {linear.iloc[-1]['std_query_time']:.3f}с\n\n"
        f"k-d дерево:\n"
        f"• При 1000 лицах: {optimized.iloc[-1]['avg_query_time']:.3f}с\n"
        f"• Стандартное отклонение: {optimized.iloc[-1]['std_query_time']:.3f}с\n\n"
        f"Улучшение производительности:\n"
        f"• При 1000 лицах: {improvement.iloc[-1]:.1f}%\n"
        f"• Среднее улучшение: {improvement.mean():.1f}%"
    )
    plt.figtext(0.02, 0.02, stats_text, fontsize=10, 
                bbox=dict(facecolor='white', alpha=0.8))
    
    # Сохраняем график с высоким разрешением
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

def main():
    # Загружаем результаты
    linear, optimized = load_results()
    
    # Строим сравнительный график
    plot_comparison(linear, optimized, 'results/comparison.png')
    
    # Выводим статистику
    print("\nСтатистика производительности:")
    print("\nЛинейный поиск:")
    print(f"Среднее время при 1000 лицах: {linear.iloc[-1]['avg_query_time']:.3f}с")
    print(f"Стандартное отклонение: {linear.iloc[-1]['std_query_time']:.3f}с")
    
    print("\nk-d дерево:")
    print(f"Среднее время при 1000 лицах: {optimized.iloc[-1]['avg_query_time']:.3f}с")
    print(f"Стандартное отклонение: {optimized.iloc[-1]['std_query_time']:.3f}с")
    
    improvement = ((linear['avg_query_time'] - optimized['avg_query_time']) / 
                  linear['avg_query_time'] * 100)
    print(f"\nУлучшение производительности при 1000 лицах: {improvement.iloc[-1]:.1f}%")
    print(f"Среднее улучшение производительности: {improvement.mean():.1f}%")

if __name__ == "__main__":
    main() 