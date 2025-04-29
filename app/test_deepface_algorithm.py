import os
import time
import numpy as np
import pandas as pd
from deepface import DeepFace
from typing import List, Dict
from pathlib import Path

def benchmark_deepface_algorithm(database_sizes: List[int] = [10, 50, 100, 250, 500, 1000],
                               num_queries: int = 10,
                               runs_per_query: int = 3) -> List[Dict]:
    """
    Тестирование производительности алгоритма с использованием DeepFace
    """
    results = []
    
    # Создаем директории для результатов
    os.makedirs("results/deepface", exist_ok=True)
    
    for db_size in database_sizes:
        print(f"\nТестирование базы данных размером {db_size} изображений...")
        
        # Генерация тестовых данных
        database_paths = [f"test_data/face_{i}.jpg" for i in range(db_size)]
        query_paths = [f"test_data/query_face_{i}.jpg" for i in range(num_queries)]
        
        query_times = []
        
        # Выполнение запросов
        for q_idx, query_path in enumerate(query_paths):
            print(f"Запрос {q_idx + 1}/{num_queries}")
            
            run_times = []
            for _ in range(runs_per_query):
                start_time = time.time()
                
                # Поиск с использованием DeepFace
                try:
                    DeepFace.find(
                        img_path=query_path,
                        db_path="test_data",
                        enforce_detection=False,
                        model_name="VGG-Face"
                    )
                    processing_time = time.time() - start_time
                except Exception as e:
                    print(f"Ошибка при обработке запроса: {e}")
                    processing_time = None
                
                if processing_time is not None:
                    run_times.append(processing_time)
            
            if run_times:
                avg_run_time = np.mean(run_times)
                query_times.append(avg_run_time)
        
        if query_times:
            # Анализ результатов
            avg_query_time = np.mean(query_times)
            std_query_time = np.std(query_times)
            
            print(f"Средн. время запроса: {avg_query_time:.6f} с")
            print(f"Станд. отклонение: {std_query_time:.6f} с")
            
            results.append({
                'database_size': db_size,
                'avg_query_time': avg_query_time,
                'std_query_time': std_query_time
            })
    
    # Сохраняем результаты в CSV
    results_df = pd.DataFrame(results)
    results_df.to_csv("results/deepface/benchmark_results.csv", index=False)
    print("\nРезультаты сохранены в results/deepface/benchmark_results.csv")
    
    return results

if __name__ == "__main__":
    benchmark_results = benchmark_deepface_algorithm()
    
    print("\nРезультаты тестирования в формате CSV:")
    print("database_size,avg_query_time,std_query_time")
    for result in benchmark_results:
        print(f"{result['database_size']},{result['avg_query_time']},{result['std_query_time']}") 