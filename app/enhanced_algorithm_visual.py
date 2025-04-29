import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def create_enhanced_detailed_plot():
    """
    Создает детальный график для улучшенного алгоритма поиска с дополнительными
    биометрическими признаками (пол, возраст).
    """
    # Загружаем данные улучшенного алгоритма
    csv_path = 'results/enhanced/benchmark_results.csv'
    
    if not os.path.exists(csv_path):
        print(f"Ошибка: файл {csv_path} не найден")
        return
    
    data = pd.read_csv(csv_path)
    
    # Создаем фигуру высокого качества
    plt.figure(figsize=(16, 10), dpi=300)
    
    # Получаем данные
    database_sizes = data['database_size']
    avg_query_times = data['avg_query_time']
    std_query_times = data['std_query_time']
    improvements = data['improvement_percent']
    
    # Основной график времени выполнения запроса
    ax1 = plt.subplot(111)
    
    # Строим основной график времени запроса
    line = ax1.plot(database_sizes, avg_query_times, 
             marker='^', label='Среднее время запроса', 
             linewidth=3, markersize=12, color='#1E88E5')
    
    # Добавляем доверительные интервалы
    ax1.fill_between(database_sizes,
                   avg_query_times - std_query_times,
                   avg_query_times + std_query_times,
                   alpha=0.3, color='#1E88E5', 
                   label='Стандартное отклонение (±σ)')
    
    # Создаем вторую ось Y для процента улучшения
    ax2 = ax1.twinx()
    improvement_line = ax2.plot(database_sizes, improvements, 
                               marker='o', label='Улучшение (%)', 
                               linewidth=3, markersize=10, 
                               linestyle='--', color='#FF5722')
    
    # Добавляем аннотации с точными значениями
    for i, (db_size, time, std_dev, imp) in enumerate(zip(database_sizes, avg_query_times, std_query_times, improvements)):
        ax1.annotate(f'{time:.6f}±{std_dev:.6f}с',
                  (db_size, time),
                  xytext=(10, -20 if i % 2 == 0 else 10), 
                  textcoords='offset points',
                  color='#1E88E5', fontsize=11,
                  bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#1E88E5", alpha=0.8))
        
        ax2.annotate(f'{imp:.1f}%',
                  (db_size, imp),
                  xytext=(-20, 10 if i % 2 == 0 else -20), 
                  textcoords='offset points',
                  color='#FF5722', fontsize=11,
                  bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#FF5722", alpha=0.8))
    
    # Настраиваем оси и заголовки
    ax1.set_xlabel('Размер базы данных (количество лиц)', fontsize=14, labelpad=10)
    ax1.set_ylabel('Время запроса (секунды)', fontsize=14, labelpad=10, color='#1E88E5')
    ax2.set_ylabel('Улучшение относительно линейного поиска (%)', fontsize=14, labelpad=15, color='#FF5722')
    
    plt.title('Детальный анализ производительности улучшенного алгоритма\nс дополнительными биометрическими признаками', 
             fontsize=16, pad=20)
    
    # Настраиваем тики осей
    ax1.tick_params(axis='y', labelcolor='#1E88E5', labelsize=12)
    ax2.tick_params(axis='y', labelcolor='#FF5722', labelsize=12)
    ax1.tick_params(axis='x', labelsize=12)
    
    # Добавляем сетку
    ax1.grid(True, linestyle='--', alpha=0.6)
    
    # Объединяем легенды с обеих осей
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', 
              fontsize=12, framealpha=0.95)
    
    # Добавляем текстовый блок с анализом производительности
    min_time_idx = np.argmin(avg_query_times)
    max_improvement_idx = np.argmax(improvements)
    
    stats_text = (
        f"Анализ производительности улучшенного алгоритма с биометрическими признаками:\n\n"
        f"• Минимальное время запроса: {avg_query_times[min_time_idx]:.6f}с при размере БД {database_sizes[min_time_idx]} лиц\n"
        f"• Максимальное улучшение: {improvements[max_improvement_idx]:.1f}% при размере БД {database_sizes[max_improvement_idx]} лиц\n"
        f"• Среднее время запроса: {avg_query_times.mean():.6f}с\n"
        f"• Среднее улучшение: {improvements.mean():.1f}%\n\n"
        f"Характеристики алгоритма:\n"
        f"• Использует k-d дерево в качестве основы для быстрого поиска\n"
        f"• Дополнительно учитывает биометрические признаки (пол, возраст)\n"
        f"• Временная сложность: O(log n) с небольшими дополнительными вычислениями\n"
        f"• Повышенная точность идентификации за счет биометрических данных"
    )
    
    plt.figtext(0.15, 0.02, stats_text, fontsize=12, 
                bbox=dict(facecolor='white', edgecolor='#888888', boxstyle='round,pad=1.0', alpha=0.95))
    
    # Создаем директорию для сохранения, если она не существует
    os.makedirs('results/enhanced', exist_ok=True)
    
    # Сохраняем график с высоким разрешением в нескольких форматах
    output_png = 'results/enhanced/detailed_performance.png'
    output_jpg = 'results/enhanced/detailed_performance.jpg'
    output_pdf = 'results/enhanced/detailed_performance.pdf'
    
    plt.tight_layout()
    plt.savefig(output_png, dpi=300, bbox_inches='tight')
    plt.savefig(output_jpg, dpi=300, bbox_inches='tight')
    plt.savefig(output_pdf, bbox_inches='tight')
    
    print(f"Детальный график улучшенного алгоритма сохранен в:")
    print(f"PNG: {output_png}")
    print(f"JPG: {output_jpg}")
    print(f"PDF: {output_pdf}")
    
    plt.close()

if __name__ == "__main__":
    create_enhanced_detailed_plot() 