from benchmark import Benchmark
from face_processor import FaceProcessor
import os

def main():
    # Создаем директории для результатов и тестовых данных
    for dir_name in ['results', 'test_data']:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        
    # Инициализируем процессор лиц и бенчмарк
    processor = FaceProcessor()
    benchmark = Benchmark(processor)
    
    # Генерируем тестовые данные
    print("Генерация тестовых данных...")
    benchmark.generate_test_data(num_users=1000)  # Генерируем максимальное количество
    
    # Запускаем тестирование
    print("Запуск тестирования производительности...")
    results = benchmark.run_benchmark(
        database_sizes=[10, 50, 100, 250, 500, 1000],
        num_queries=100
    )
    
    # Сохраняем результаты
    print("Сохранение результатов...")
    benchmark.save_results(results, 'results/benchmark_results.csv')
    
    # Строим графики
    print("Построение графиков...")
    benchmark.plot_results(results, 'results/benchmark_plot.png')
    benchmark.create_animation('results/benchmark_animation.gif')
    
    print("Тестирование завершено!")
    print("Результаты сохранены в директории 'results'")

if __name__ == '__main__':
    main() 