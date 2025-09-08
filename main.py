from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from database.db import init_database
from database.queries import create_user, get_user, get_all_products, delete_product
from database.seeds import seed_products

# Токен от BotFather
TOKEN = "7514093364:AAGGHIabFBhurOFDtQW-92_wOA6e4x8MZuc"

SERVICES = {
    'basic': {'name': 'Хуй', 'price': 100000},   # 1000 руб
    'premium': {'name': 'Пенис', 'price': 250000}, # 2500 руб
    'vip': {'name': 'Член', 'price': 500000},     # 5000 руб
}

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_user = update.effective_user
    # Вызываем функцию создания/обновления пользователя в БД
    create_user(
        user_id=telegram_user.id,
        username=telegram_user.username,
        first_name=telegram_user.first_name,
        last_name=telegram_user.last_name
    )

    # Проверяем, сохранился ли пользователь
    saved_user = get_user(telegram_user.id)  # Эту функцию ты должен реализовать в database/queries.py
    if saved_user:
        print(f"✅ Пользователь сохранён в БД: {saved_user}")
    else:
        print("❌ Ошибка: пользователь не найден в БД после сохранения")

    keyboard = [
        [InlineKeyboardButton("💰 Услуги и цены", callback_data="services")],
        [InlineKeyboardButton("ℹ️ Помощь", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(

        f"Привет, {telegram_user.first_name or telegram_user.username or 'друг'}! 👋\n"
        "Я бот для оплаты услуг.\n\n"
        "Выберите опцию:",
        reply_markup=reply_markup
    )

# Обработчик выбора товара
async def show_services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Получаем товары из базы данных
    products = get_all_products()  # 👈 Вызываем функцию из database/queries.py

    # Формируем кнопки на основе товаров из БД
    keyboard = []
    for product in products:
        # product — это объект Product (из dataclass) или словарь
        # Проверь, как именно выглядит product в твоём случае
        price_rub = product['price'] / 100  # Переводим из копеек в рубли
        keyboard.append([
            InlineKeyboardButton(
                f"{product['name']} - {price_rub:.2f} руб",  # 👈 Используем ключи
                callback_data=f"buy_{product['id']}"  # ID товара для покупки
            )
        ])

    # Добавляем кнопку "Назад"
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="back")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем сообщение с динамическим текстом
    await query.edit_message_text(
        "🎯 Выберите товар:",
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Создаём кнопку "Назад"
    keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Меняем текущее сообщение на помощь + кнопка назад
    await query.edit_message_text(
        text="🆘 Помощь:\n\n"
             "Бро, за помощью можешь обращаться сюда @zephiel",
        reply_markup=reply_markup
    )

# Обработчик "Назад"
async def handle_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("💰 Услуги и цены", callback_data="services")],
        [InlineKeyboardButton("ℹ️ Помощь", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        "👋 Добро пожаловать! Выберите опцию:",
        reply_markup=reply_markup
    )

# Главная функция
def main():
    print("Инициализация базы данных...")
    init_database()
    print("Готово! Файл базы данных создан в папке data/")


    # Создаём приложение
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(show_services, pattern="^services$"))
    application.add_handler(CallbackQueryHandler(help_command, pattern="^help$"))
    application.add_handler(CallbackQueryHandler(handle_back, pattern="^back$"))

    # Запускаем бота
    print("✅ Бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()