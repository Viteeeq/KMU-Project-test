from app.optimized_face_processor import OptimizedFaceProcessor
from app.optimized_benchmark import OptimizedBenchmark
import os

def main():
    # Создаем директорию для результатов, если её нет
    if not os.path.exists('results'):
        os.makedirs('results')
        
    # Инициализируем процессор и бенчмарк
    processor = OptimizedFaceProcessor()
    benchmark = OptimizedBenchmark(processor)
    
    # Запускаем тестирование
    database_sizes = [10, 50, 100, 250, 500, 1000]
    results = benchmark.run_benchmark(database_sizes, 100)
    
    # Сохраняем и визуализируем результаты
    benchmark.save_results(results, 'results/optimized_benchmark_results.csv')
    benchmark.plot_results(results, 'results/optimized_benchmark_results.png')
    benchmark.create_animation('results/optimized_benchmark_animation.gif')
    
    print("Тестирование завершено. Результаты сохранены в директории 'results'")

if __name__ == "__main__":
    main() 