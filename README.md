# Telegram Shop Bot

Небольшой тестовый интернет‑магазин на базе Telegram‑бота.  
Цель проекта — практика работы с Telegram Bot API, базой данных и интеграцией оплат.

## Структура проекта
- main.py — точка входа: инициализация БД и запуск бота.
- config.py — локальные настройки и токены (не коммитить реальные значения).
- requirements.txt — зависимости (см. ниже).
- .gitignore — исключаемые файлы/папки.
- bot/ — логика бота (handlers.py, keyboards.py, messages.py).
- database/ — работа с БД (db.py, models.py, queries.py).
- payment/ — интеграция с платёжными провайдерами (telegram_payments.py, tinkoff.py).
- utils/ — вспомогательные функции.
- data/ — (опционально) локальные данные, дампы, seed-файлы.
- tests/ — тесты.

## Быстрый старт (локально)
1. Клонируйте репозиторий.
2. Создайте виртуальное окружение и активируйте его:
   - python -m venv venv
   - Windows: venv\Scripts\activate
   - macOS/Linux: source venv/bin/activate
3. Установите зависимости:
   - pip install -r requirements.txt
4. Создайте локальный config.py (скопируйте шаблон ниже) и заполните токены:
```python
# config.py (пример, НЕ коммитить)
BOT_TOKEN = "ВАШ_BOT_TOKEN"
TELEGRAM_PROVIDER_TOKEN = "ВАШ_PROVIDER_TOKEN"
DATABASE_PATH = "database/shop.db"
DEBUG = True
Инициализируйте БД и запустите бота:
python main.py