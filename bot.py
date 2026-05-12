import os
import asyncio
import logging
from datetime import datetime
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
MINI_APP_URL = os.getenv("MINI_APP_URL")
PHOTO_URL = os.getenv("PHOTO_URL", "https://i.ibb.co/VWrpJfGD/2026-04-17-235426316.png")
RENDER_URL = "https://jelly-yuvi.onrender.com"

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def send_new_user_notification(user: types.User):
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
    user = message.from_user
    await send_new_user_notification(user)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛒 ДО ПОКУПОК", web_app=types.WebAppInfo(url=MINI_APP_URL))]
        ]
    )

    welcome_text = (
        f"🌟 <b>Раді вітати вас у нашому магазині!</b>\n\n"
        f"Добрий день 👋 {message.from_user.first_name}! "
        f"Асортимент та актуальні ціни залежать від вашого регіону. "
        f"Щоб отримати актуальний прайс — тисни кнопку нижче 👇"
    )

    await message.answer_photo(
        photo=PHOTO_URL,
        caption=welcome_text,
        reply_markup=keyboard
    )
    logger.info(f"User {user.id} started the bot")


async def main():
    webhook_path = f"/webhook/{BOT_TOKEN}"
    webhook_url = f"{RENDER_URL}{webhook_path}"

    await bot.set_webhook(url=webhook_url, drop_pending_updates=True)
    logger.info(f"Webhook set: {webhook_url}")

    app = web.Application()
    app.router.add_get("/", lambda r: web.Response(text="OK"))
    app.router.add_get("/health", lambda r: web.Response(text="OK"))
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=webhook_path)

    port = int(os.getenv("PORT", 10000))
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", port).start()
    logger.info(f"Bot started on port {port}")

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
