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

# ====== БОТ 1 (украинский) ======
BOT_TOKEN_1 = os.getenv("BOT_TOKEN_1")
CHANNEL_ID_1 = int(os.getenv("CHANNEL_ID_1"))
BUTTON_URL_1 = os.getenv("BUTTON_URL_1")
PHOTO_URL_1 = os.getenv("PHOTO_URL_1", "https://i.ibb.co/VWrpJfGD/2026-04-17-235426316.png")

# ====== БОТ 2 (русский) ======
BOT_TOKEN_2 = os.getenv("BOT_TOKEN_2")
CHANNEL_ID_2 = int(os.getenv("CHANNEL_ID_2"))
BUTTON_URL_2 = os.getenv("BUTTON_URL_2")
PHOTO_URL_2 = os.getenv("PHOTO_URL_2", "https://i.ibb.co/1GKzZvFn/photo-2026-05-12-22-43-22.jpg")

RENDER_URL = "https://jelly-yuvi.onrender.com"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot1 = Bot(token=BOT_TOKEN_1, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
bot2 = Bot(token=BOT_TOKEN_2, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp1 = Dispatcher()
dp2 = Dispatcher()


# ====== ХЕНДЛЕРЫ БОТА 1 (украинский) ======
async def notify_1(user: types.User):
    try:
        username = f"@{user.username}" if user.username else "немає юзернейму"
        time_str = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        await bot1.send_message(CHANNEL_ID_1,
            f"🆕 <b>Новий користувач зайшов у бот 1</b>\n\n"
            f"👤 Профіль: tg://user?id={user.id}\n"
            f"📝 Ім'я: {user.full_name} ({username})\n"
            f"🕐 Час: {time_str}"
        )
    except Exception as e:
        logger.error(f"Bot1 notify error: {e}")

@dp1.message(CommandStart())
async def start_bot1(message: types.Message):
    await notify_1(message.from_user)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 ДО ПОКУПОК", url=BUTTON_URL_1)]
    ])
    await message.answer_photo(
        photo=PHOTO_URL_1,
        caption=(
            f"🌟 <b>Раді вітати вас у нашому магазині!</b>\n\n"
            f"Добрий день 👋 {message.from_user.first_name}! "
            f"Асортимент та актуальні ціни залежать від вашого регіону. "
            f"Щоб отримати актуальний прайс — тисни кнопку нижче 👇"
        ),
        reply_markup=keyboard
    )


# ====== ХЕНДЛЕРЫ БОТА 2 (русский) ======
async def notify_2(user: types.User):
    try:
        username = f"@{user.username}" if user.username else "нет юзернейма"
        time_str = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        await bot2.send_message(CHANNEL_ID_2,
            f"🆕 <b>Новый пользователь зашёл в бот РБ</b>\n\n"
            f"👤 Профиль: tg://user?id={user.id}\n"
            f"📝 Имя: {user.full_name} ({username})\n"
            f"🕐 Время: {time_str}"
        )
    except Exception as e:
        logger.error(f"Bot2 notify error: {e}")

@dp2.message(CommandStart())
async def start_bot2(message: types.Message):
    await notify_2(message.from_user)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 К ПОКУПКАМ", url=BUTTON_URL_2)]
    ])
    await message.answer_photo(
        photo=PHOTO_URL_2,
        caption=(
            f"🌟 <b>Рады вітаць вас у нашай краме!</b>\n\n"
    f"Добры дзень 👋 {message.from_user.first_name}! "
    f"Асартымент і актуальныя цэны залежаць ад вашага рэгіёна. "
    f"Каб атрымаць актуальны прайс — цісні кнопку ніжэй 👇"
        ),
        reply_markup=keyboard
    )


# ====== ЗАПУСК ======
async def main():
    path1 = f"/webhook/{BOT_TOKEN_1}"
    path2 = f"/webhook/{BOT_TOKEN_2}"

    await bot1.set_webhook(url=f"{RENDER_URL}{path1}", drop_pending_updates=True)
    await bot2.set_webhook(url=f"{RENDER_URL}{path2}", drop_pending_updates=True)
    logger.info("Webhooks set for both bots")

    app = web.Application()
    app.router.add_get("/", lambda r: web.Response(text="OK"))
    app.router.add_get("/health", lambda r: web.Response(text="OK"))

    SimpleRequestHandler(dispatcher=dp1, bot=bot1).register(app, path=path1)
    SimpleRequestHandler(dispatcher=dp2, bot=bot2).register(app, path=path2)

    port = int(os.getenv("PORT", 10000))
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", port).start()
    logger.info(f"Both bots started on port {port}")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
