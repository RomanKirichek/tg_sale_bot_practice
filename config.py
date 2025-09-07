# config.py
# НЕ храните реальные ключи в репозитории.
from pathlib import Path
import os

# Токен бота получаете у @BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN", "7514093364:AAGGHIabFBhurOFDtQW-92_wOA6e4x8MZuc")

# Провайдер платежей (получается через @BotFather)
TELEGRAM_PROVIDER_TOKEN = os.getenv("TELEGRAM_PROVIDER_TOKEN", "REPLACE_PROVIDER_TOKEN")

# Путь до файла БД
BASE_DIR = Path(__file__).parent
DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "database" / "shop.db"))

# Режим отладки
DEBUG = os.getenv("DEBUG", "1") == "1"
