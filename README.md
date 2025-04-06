# Система биометрической идентификации с оптимизированным поиском

Проект направлен на повышение скорости и точности поиска пользователя в биометрических системах.

## Основные возможности

- Использование PostgreSQL для хранения биометрических данных
- Реализация k-d дерева для оптимизации поиска
- Интеграция DeepFace для извлечения дополнительных признаков (пол, возраст)
- Тестирование производительности на различных объемах данных
- Генерация тестовых данных для оценки эффективности

## Требования

- Python 3.8+
- PostgreSQL
- OpenCV
- DeepFace
- PyQt5
- NumPy
- Pandas
- Matplotlib
- scikit-learn

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Настройте базу данных PostgreSQL:
```sql
CREATE DATABASE postamat;
CREATE USER user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE postamat TO user;
```

## Структура проекта

- `app/database.py` - Работа с PostgreSQL
- `app/biometric_processor.py` - Обработка биометрических данных
- `app/benchmark.py` - Тестирование производительности
- `app/data_generator.py` - Генерация тестовых данных

## Использование

1. Генерация тестовых данных:
```bash
python app/data_generator.py
```

2. Запуск тестирования производительности:
```bash
python app/benchmark.py
```

## Результаты

Результаты тестирования сохраняются в:
- `benchmark_results.csv` - Данные о производительности
- `benchmark_results.png` - Графики результатов

## Лицензия

MIT