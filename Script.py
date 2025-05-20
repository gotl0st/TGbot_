import random
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

# Константы для ConversationHandler
NAME, GAME = range(2)

def start(update: Update, context: CallbackContext) -> None:
    """Обработка команды /start"""
    user = update.effective_user
    update.message.reply_text(
        f"Привет, {user.first_name}! Я бот, который сможет скоротать твое время. Вот что я умею:\n"
        "🔮 /guessage - угадаю твой возраст по имени\n"
        "😂 /joke - расскажу анекдот\n"
        "🎮 /game - сыграем в 'Камень-ножницы-бумага'\n"
        "❌ /cancel - если надоело"
    )

def guess_age(update: Update, context: CallbackContext) -> int:
    """Начинает угадывать возраст по имени"""
    update.message.reply_text(
        "Напиши своё имя, и я угадаю твой возраст! (Или /cancel чтобы выйти)"
    )
    return NAME

def process_name(update: Update, context: CallbackContext) -> int:
    """'Угадывает' возраст (рандомно)"""
    name = update.message.text
    age_guess = random.randint(1, 300)
    update.message.reply_text(
        f"Хмм... {name}, тебе точно {age_guess} лет! 😉"
    )
    return ConversationHandler.END

def joke(update: Update, context: CallbackContext) -> None:
    """Рассказывает случайный анекдот"""
    jokes = [
        "Программист на пляже. Жена ему:\n"
        "— Дорогой, сходи в море, искупайся!\n"
        "— Ладно... unsigned char купаться = 0;",

        "— Почему программисты путают Хэллоуин и Рождество?\n"
        "— Потому что 31 OCT == 25 DEC.",

        "— Алло, это служба поддержки?\n"
        "— Да.\n"
        "— У меня чайник не работает!\n"
        "— Это к электрикам.\n"
        "— А вы кто?\n"
        "— Служба поддержки Чайников:)."
    ]
    update.message.reply_text(random.choice(jokes))

def game(update: Update, context: CallbackContext) -> int:
    """Начинает игру в камень-ножницы-бумага"""
    keyboard = [["Камень", "Ножницы", "Бумага"]]
    update.message.reply_text(
        "Выбирай: Камень, Ножницы или Бумага? (Или /cancel)",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    )
    return GAME

def play_game(update: Update, context: CallbackContext) -> int:
    """Обрабатывает выбор пользователя и определяет победителя"""
    user_choice = update.message.text.lower()
    bot_choice = random.choice(["камень", "ножницы", "бумага"])
    
    # Определение победителя
    if user_choice == bot_choice:
        result = "Ничья! 🤝"
    elif (user_choice == "камень" and bot_choice == "ножницы") or \
         (user_choice == "ножницы" and bot_choice == "бумага") or \
         (user_choice == "бумага" and bot_choice == "камень"):
        result = "Ты победил! 🎉"
    else:
        result = "Я победил! 😈"
    
    update.message.reply_text(
        f"Ты выбрал: {user_choice}\n"
        f"Я выбрал: {bot_choice}\n"
        f"{result}\n\n"
        "Сыграем ещё? /game или /start",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    """Завершает диалог"""
    update.message.reply_text(
        "Ладно, возвращайся, если захочешь повеселиться!",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def main() -> None:
    """Запуск бота"""
    updater = Updater("ВАШ TELEGRAM BOT TOKEN")  # Замените на свой токен!
    dispatcher = updater.dispatcher

    # ConversationHandler для угадывания возраста
    guess_age_conv = ConversationHandler(
        entry_points=[CommandHandler("guessage", guess_age)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, process_name)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # ConversationHandler для игры
    game_conv = ConversationHandler(
        entry_points=[CommandHandler("game", game)],
        states={
            GAME: [MessageHandler(Filters.regex("^(Камень|Ножницы|Бумага)$"), play_game)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Регистрация обработчиков
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(guess_age_conv)
    dispatcher.add_handler(CommandHandler("joke", joke))
    dispatcher.add_handler(game_conv)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()