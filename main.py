from telegram import Update, LabeledPrice, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Токен от BotFather
TOKEN = "7514093364:AAGGHIabFBhurOFDtQW-92_wOA6e4x8MZuc"

SERVICES = {
    'basic': {'name': 'Хуй', 'price': 100000},  # 1000 руб
    'premium': {'name': 'Пенис', 'price': 250000},  # 2500 руб
    'vip': {'name': 'Член', 'price': 500000},  # 5000 руб
}

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💰 Услуги и цены", callback_data="services")],
        [InlineKeyboardButton("ℹ️ Помощь", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Привет бро! Я бот для оплаты услуг.\n\n"
        "Выберите опцию:",
        reply_markup=reply_markup
    )

# Обработчик выбора товара
async def show_services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = []
    for service_id, service in SERVICES.items():
        price_rub = service['price'] / 100  # Переводим в рубли
        keyboard.append([
            InlineKeyboardButton(
                f"{service['name']} - {price_rub} руб",
                callback_data=f"buy_{service_id}"
            )
        ])

    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="back")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "🎯 Выберите услугу:\n\n"
        "• Хуй в жопе - 1000 руб\n"
        "• Пенис в горле - 2500 руб\n"
        "• Член в ухе - 5000 руб",
        reply_markup=reply_markup
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❓ Помощь по боту:\n\n"
        "• Выберите услугу для оплаты\n"
        "• Оплатите через безопасную систему\n"
        "• Получите подтверждение и услугу\n\n"
        "Для начала работы нажмите /start"
    )

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
    # Создаём приложение
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(show_services, pattern="^services$"))
    application.add_handler(CallbackQueryHandler(help_command, pattern="^help$"))
    application.add_handler(CallbackQueryHandler(handle_back, pattern="^back$"))

    # Запускаем бота
    print("Бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()
