# database/seeds.py
from .queries import add_product

def seed_products():
    """Добавление тестовых товаров."""
    print("Заполняем базу тестовыми товарами...")
    add_product("Зипка модная", 6000000)
    add_product("Кофта норм", 300000)
    add_product("Батины семейники", 250000)
    print("✅ Товары добавлены")

if __name__ == "__main__":
    seed_products()