# CSV Processor

Скрипт process_csv.py позволяет фильтровать и агрегировать данные из CSV-файла.

**Примеры запуска:**

Фильтрация:
```
python3 process_csv.py example.csv --where "price>100"
```
Агрегация:
```
python3 process_csv.py example.csv --aggregate "price=avg"
```
Фильтрация и агрегация вместе:
```
python3 process_csv.py example.csv --where "brand=xiaomi" --aggregate "price=max"
```

Для тестирования:
```
pytest test_process_csv.py
```

