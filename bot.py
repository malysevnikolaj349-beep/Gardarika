# bot.py
import logging
import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

# Импортируем наши модули
from gardarika.database.operations import (
    add_user_if_not_exists,
    get_character_by_user_id,
    create_character,
)
from gardarika.character.character import Character
from gardarika.character.attributes import PrimaryAttribute

# Включаем логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Определяем состояния для диалога
CHOOSING_NAME, CHOOSING_CLASS, CHOOSING_FACTION = range(3)

# --- Функции-обработчики команд ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает команду /start, регистрирует пользователя."""
    user = update.effective_user
    add_user_if_not_exists(user.id)
    await update.message.reply_html(
        f"Привет, {user.mention_html()}!\n"
        "Добро пожаловать в мир Гардарики. "
        "Чтобы создать персонажа, используйте команду /create_character.\n"
        "Чтобы посмотреть профиль, используйте /profile."
    )

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает профиль персонажа с расширенными характеристиками."""
    user_id = update.effective_user.id
    character_data = get_character_by_user_id(user_id)

    if character_data:
        # Создаем полноценный объект персонажа из данных БД
        # Все вторичные характеристики будут рассчитаны автоматически
        player = Character.from_db_data(character_data)
        await update.message.reply_html(str(player))
    else:
        await update.message.reply_text(
            "У вас еще нет персонажа. "
            "Используйте команду /create_character, чтобы создать его."
        )

# --- Логика создания персонажа ---

async def create_character_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начинает диалог создания персонажа."""
    user_id = update.effective_user.id
    if get_character_by_user_id(user_id):
        await update.message.reply_text("У вас уже есть персонаж. Вы можете посмотреть его профиль командой /profile.")
        return ConversationHandler.END

    await update.message.reply_text("Создание нового персонажа. Как его будут звать?")
    return CHOOSING_NAME

async def choose_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Получает имя персонажа и запрашивает класс."""
    context.user_data['name'] = update.message.text

    keyboard = [
        [InlineKeyboardButton("Воин", callback_data="воин")],
        [InlineKeyboardButton("Волхв", callback_data="волхв")],
        [InlineKeyboardButton("Охотник", callback_data="охотник")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Отличное имя! Теперь выбери класс:", reply_markup=reply_markup)
    return CHOOSING_CLASS

async def choose_class(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Получает класс и запрашивает фракцию."""
    query = update.callback_query
    await query.answer()
    context.user_data['class'] = query.data

    keyboard = [
        [InlineKeyboardButton("Киевское Княжество", callback_data="kiev")],
        [InlineKeyboardButton("Новгородская Республика", callback_data="novgorod")],
        [InlineKeyboardButton("Лесные Племена", callback_data="forest_tribes")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text="Класс выбран. К какой фракции примкнешь?", reply_markup=reply_markup)
    return CHOOSING_FACTION

async def choose_faction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Получает фракцию, создает персонажа и завершает диалог."""
    query = update.callback_query
    await query.answer()
    context.user_data['faction'] = query.data

    user_id = update.effective_user.id
    char_data = context.user_data

    try:
        # Создаем экземпляр персонажа для получения начальных статов
        player = Character(char_data['name'], char_data['class'], char_data['faction'])

        # Готовим данные для записи в БД
        stats_for_db = {
            'health': player.health,
            'mana': player.mana,
            'strength': player.primary_attributes.get(PrimaryAttribute.STRENGTH, 0),
            'dexterity': player.primary_attributes.get(PrimaryAttribute.DEXTERITY, 0),
            'wisdom': player.primary_attributes.get(PrimaryAttribute.WISDOM, 0),
            'endurance': player.primary_attributes.get(PrimaryAttribute.ENDURANCE, 0),
            'charisma': player.primary_attributes.get(PrimaryAttribute.CHARISMA, 0),
        }

        # Сохраняем в БД
        create_character(user_id, player.name, player.character_class.name, player.faction['name'], stats_for_db)

        await query.edit_message_text(text=f"Персонаж создан!\n\n{player}", parse_mode='HTML')
    except (ValueError, KeyError) as e:
        await query.edit_message_text(text=f"Произошла ошибка при создании персонажа: {e}")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отменяет и завершает диалог."""
    await update.message.reply_text("Создание персонажа отменено.")
    return ConversationHandler.END

# --- Главная функция ---

def main() -> None:
    """Запускает бота."""
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TELEGRAM_TOKEN:
        print("Ошибка: Токен Telegram-бота не найден.")
        print("Пожалуйста, установите переменную окружения TELEGRAM_TOKEN.")
        return

    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Диалог создания персонажа
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("create_character", create_character_start)],
        states={
            CHOOSING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_name)],
            CHOOSING_CLASS: [CallbackQueryHandler(choose_class)],
            CHOOSING_FACTION: [CallbackQueryHandler(choose_faction)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("profile", profile))

    print("Бот запущен...")
    application.run_polling()
    print("Бот остановлен.")

if __name__ == "__main__":
    main()
