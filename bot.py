import asyncio
import logging
import os
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Конфігурація
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "-1003655775830"))
MINI_APP_URL = os.getenv("MINI_APP_URL", "https://ltt.wuaze.com")
PHOTO_URL = os.getenv("PHOTO_URL", "https://i.ibb.co/VWrpJfGD/2026-04-17-235426316.png")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set")

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Створення бота та диспетчера
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

async def send_new_user_notification(user: types.User):
    """Надсилає повідомлення про нового користувача в канал"""
    try:
        username = f"@{user.username}" if user.username else "немає юзернейму"
        profile_link = f"tg://user?id={user.id}"
        time_str = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        
        message = (
            f"🆕 <b>Новий користувач зайшов у бот</b>\n\n"
            f"👤 Профіль: {profile_link}\n"
            f"📝 Ім'я: {user.full_name} ({username})\n"
            f"🕐 Час: {time_str}"
        )
        
        await bot.send_message(CHANNEL_ID, message)
        logger.info(f"Notification sent for user {user.id}")
    except Exception as e:
        logger.error(f"Error sending notification: {e}")

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    """Обробка команди /start"""
    user = message.from_user
    
    # Надсилаємо повідомлення про нового користувача в канал
    await send_new_user_notification(user)
    
    # Створюємо клавіатуру з кнопкою
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛒 ДО ПОКУПОК", web_app=types.WebAppInfo(url=MINI_APP_URL))]
        ]
    )
    
    # Привітальне повідомлення з фото
    welcome_text = (
        "👋 <b>Вітаємо в Jelly Store!</b>\n\n"
        "🔥 <b>Найкращі ціни на ринку</b>\n"
        "✅ <b>Перевірена часом якість</b>\n\n"
        "Натисніть кнопку нижче, щоб переглянути прайс та оформити замовлення!👇\n\n"
    )
    
    await message.answer_photo(
        photo=PHOTO_URL,
        caption=welcome_text,
        reply_markup=keyboard
    )
    
    logger.info(f"User {user.id} started the bot")

async def main():
    """Головна функція для запуску бота"""
    # Видалення вебхуків, якщо є
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Bot started polling")
    
    # Запуск полінгу
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")
