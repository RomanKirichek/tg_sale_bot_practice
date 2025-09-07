import sqlite3
import os
from typing import List, Dict, Optional


def get_connection():
    """Создание подключения к базе данных"""
    # Создаем папку data, если её нет
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Позволяет обращаться к колонкам по имени
    return conn