import os
import time
import numpy as np
import pandas as pd
import face_recognition
from typing import List, Dict
from pathlib import Path

def benchmark_face_recognition_algorithm(database_sizes: List[int] = [10, 50, 100, 250, 500, 1000],
                                      num_queries: int = 10,
                                      runs_per_query: int = 3) -> List[Dict]:
    """
    Тестирование производительности алгоритма с использованием face_recognition
    """
    results = []
    
    # Создаем директории для результатов
    os.makedirs("results/face_recognition", exist_ok=True)
    
    for db_size in database_sizes:
        print(f"\nТестирование базы данных размером {db_size} изображений...")
        
        # Загрузка и кодирование изображений из базы данных
        database_encodings = []
        for i in range(db_size):
            try:
                image = face_recognition.load_image_file(f"test_data/face_{i}.jpg")
                encoding = face_recognition.face_encodings(image)[0]
                database_encodings.append(encoding)
            except Exception as e:
                print(f"Ошибка при обработке изображения face_{i}.jpg: {e}")
        
        query_times = []
        
        # Выполнение запросов
        for q_idx in range(num_queries):
            print(f"Запрос {q_idx + 1}/{num_queries}")
            
            try:
                # Загрузка тестового изображения
                query_image = face_recognition.load_image_file(f"test_data/query_face_{q_idx}.jpg")
                query_encoding = face_recognition.face_encodings(query_image)[0]
                
                run_times = []
                for _ in range(runs_per_query):
                    start_time = time.time()
                    
                    # Сравнение с базой данных
                    matches = face_recognition.compare_faces(database_encodings, query_encoding)
                    face_distances = face_recognition.face_distance(database_encodings, query_encoding)
                    
                    processing_time = time.time() - start_time
                    run_times.append(processing_time)
                
                avg_run_time = np.mean(run_times)
                query_times.append(avg_run_time)
                
            except Exception as e:
                print(f"Ошибка при обработке запроса {q_idx}: {e}")
        
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
    results_df.to_csv("results/face_recognition/benchmark_results.csv", index=False)
    print("\nРезультаты сохранены в results/face_recognition/benchmark_results.csv")
    
    return results

if __name__ == "__main__":
    benchmark_results = benchmark_face_recognition_algorithm()
    
    print("\nРезультаты тестирования в формате CSV:")
    print("database_size,avg_query_time,std_query_time")
    for result in benchmark_results:
        print(f"{result['database_size']},{result['avg_query_time']},{result['std_query_time']}") 