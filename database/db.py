# database/db.py
import sqlite3
import os
from config import DATABASE_PATH


def get_connection():
    """Создание подключения к базе данных SQLite."""
    # Создаем папку, если её нет
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

    # Подключаемся к БД
    conn = sqlite3.connect(DATABASE_PATH)

    # Это позволяет обращаться к полям по имени, а не только по индексу
    conn.row_factory = sqlite3.Row

    return conn


def init_database():
    """Создание всех необходимых таблиц в базе данных."""
    conn = get_connection()
    cursor = conn.cursor()

    print("Создаём таблицы в базе данных...")

    # 1. Таблица пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("✓ Таблица 'users' создана")

    # 2. Таблица товаров
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL,  -- в копейках
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("✓ Таблица 'products' создана")

    # 3. Таблица корзины
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER DEFAULT 1,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
        )
    ''')
    print("✓ Таблица 'cart' создана")

    # 4. Таблица заказов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            total_amount INTEGER NOT NULL,  -- в копейках
            status TEXT DEFAULT 'pending',  -- pending, paid, cancelled
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    print("✓ Таблица 'orders' создана")

    # 5. Таблица товаров в заказе
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price INTEGER NOT NULL,  -- цена на момент покупки
            FOREIGN KEY (order_id) REFERENCES orders (id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    print("✓ Таблица 'order_items' создана")

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()
    print("✅ База данных инициализирована успешно!")

