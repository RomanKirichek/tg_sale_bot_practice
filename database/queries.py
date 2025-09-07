"""
Модуль с функциями для работы с базой данных.
Содержит функции для добавления/получения пользователей, товаров, корзины и заказов.
"""

import sqlite3
from typing import List, Dict, Optional
from config import DATABASE_PATH


def get_connection():
    """Создаёт и возвращает подключение к базе данных."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Позволяет обращаться к полям по имени
    return conn

def create_user(user_id: int, username: str = None, first_name: str = None, last_name: str = None):
    """Добавляет или обновляет пользователя в базе данных."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, username, first_name, last_name)
        VALUES (?, ?, ?, ?)
    ''', (user_id, username, first_name, last_name))
    conn.commit()
    conn.close()


def get_user(user_id: int) -> Optional[Dict]:
    """Возвращает информацию о пользователе по его user_id."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

#----------------------------------------

def add_product(name: str, price: int, description: str = "", image_url: str = None):
    """Добавляет новый товар в базу данных."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO products (name, description, price, image_url)
        VALUES (?, ?, ?, ?)
    ''', (name, description, price, image_url))
    product_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return product_id


def get_all_products() -> List[Dict]:
    """Возвращает список всех товаров."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_product_by_id(product_id: int) -> Optional[Dict]:
    """Возвращает товар по его ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

#----------------------------------------
def add_to_cart(user_id: int, product_id: int, quantity: int = 1):
    """Добавляет товар в корзину пользователя."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO cart (user_id, product_id, quantity)
        VALUES (?, ?, ?)
    ''', (user_id, product_id, quantity))
    conn.commit()
    conn.close()


def get_user_cart(user_id: int) -> List[Dict]:
    """Возвращает содержимое корзины пользователя."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.id, p.name, p.price, c.quantity
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = ?
    ''', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def clear_user_cart(user_id: int):
    """Очищает корзину пользователя."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cart WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

#----------------------------------------

def create_order(user_id: int, total_amount: int) -> int:
    """Создаёт новый заказ и возвращает его ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO orders (user_id, total_amount, status)
        VALUES (?, ?, 'pending')
    ''', (user_id, total_amount))
    order_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return order_id


def update_order_status(order_id: int, status: str):
    """Обновляет статус заказа."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE orders SET status = ? WHERE id = ?
    ''', (status, order_id))
    conn.commit()
    conn.close()


def get_order_by_id(order_id: int) -> Optional[Dict]:
    """Возвращает информацию о заказе по его ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None