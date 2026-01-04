# Лабораторная работа 7: Архитектура, слои и DDD-lite

Реализация системы оплаты заказа с использованием слоистой архитектуры и принципов DDD-lite.

## Структура проекта

- **domain/**: Доменная модель и бизнес-правила
  - `models.py`: Сущности, Value Objects, агрегаты
  - `exceptions.py`: Доменные исключения

- **application/**: Use-case слой
  - `use_cases.py`: Use-case оплаты заказа и интерфейсы

- **infrastructure/**: Инфраструктурный слой
  - `repositories.py`: In-memory репозиторий
  - `gateways.py`: Fake платежный шлюз

- **tests/**: Тесты
  - `test_domain.py`: Тесты доменной модели
  - `test_use_cases.py`: Тесты use-case

## Использование

### Запуск тестов

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск всех тестов
pytest tests/
