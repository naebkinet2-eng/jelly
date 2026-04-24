# Jelly Store Telegram Bot

Telegram бот для Jelly Store з міні-апом та відправкою повідомлень про нових користувачів в канал.

## Функції

- 🛒 Кнопка "За покупками" що відкриває Telegram Mini App
- 📸 Привітальне повідомлення з фото та продаючим текстом
- 📢 Автоматичне повідомлення в канал про кожного нового користувача
- 🇺🇦 Повністю український інтерфейс

## Вимоги

- Python 3.9+
- aiogram 3.4.1

## Локальний запуск

1. Встановіть залежності:
```bash
pip install -r requirements.txt
```

2. Запустіть бота:
```bash
python bot.py
```

## Налаштування

Перш ніж запускати бота, переконайтеся що:
- Бот має права адміністратора в каналі для відправки повідомлень
- Міні-ап налаштований в @BotFather

## Розгортання на GitHub

### 1. Створіть репозиторій

1. Зайдіть на [GitHub](https://github.com) і створіть новий репозиторій
2. Завантажте файли:
   - `bot.py`
   - `requirements.txt`
   - `README.md`
   - `.render.yaml`

### 2. Налаштування GitHub Actions (опціонально)

Створіть файл `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Render

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Render
        run: echo "Deploy to Render via webhook"
```

## Розгортання на Render

### 1. Створіть акаунт на Render

1. Зайдіть на [render.com](https://render.com)
2. Зареєструйтесь або увійдіть

### 2. Підключіть GitHub репозиторій

1. Натисніть "New +"
2. Виберіть "Web Service"
3. Підключіть ваш GitHub репозиторій

### 3. Налаштування Web Service

**Build & Deploy:**

- **Name:** jelly-store-bot
- **Region:** Frankfurt (або найближчий до вас)
- **Branch:** main
- **Root Directory:** (залиште порожнім)
- **Runtime:** Python 3
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python bot.py`

**Environment Variables:**

Додайте наступні змінні середовища (не обов'язково, якщо вони вже в коді):
- `BOT_TOKEN`: `8312721839:AAETwf44GH1IU09uFYeCianp-2CSNcpZTBA`
- `CHANNEL_ID`: `-1003655775830`
- `MINI_APP_URL`: `https://ltt.wuaze.com`
- `PHOTO_URL`: `https://i.ibb.co/VWrpJfGD/2026-04-17-235426316.png`

### 4. Налаштування без засинання

Render автоматично перезапускає сервіс якщо він падає. Для додаткової надійності:

1. У налаштуваннях Web Service:
   - **Instance Type:** Free (або Starter для кращої продуктивності)
   - **Health Check Path:** (залиште порожнім для бота)

### 5. Альтернатива: Використання .render.yaml

Файл `.render.yaml` вже включений в проект. Render автоматично розпізнає його при підключенні репозиторію.

## Важливі примітки

1. **Права бота в каналі:** Бот повинен бути адміністратором каналу для відправки повідомлень
2. **Міні-ап:** Переконайтеся що URL міні-апа налаштований в @BotFather
3. **Токен безпеки:** Ніколи не публікуйте токен бота в публічних репозиторіях. Використовуйте Environment Variables.

## Моніторинг

Після розгортання:
- Перевірте логи в панелі Render
- Переконайтеся що бот відповідає на команду /start
- Перевірте що повідомлення приходять в канал

## Підтримка

Якщо виникли проблеми:
1. Перевірте логи в Render
2. Переконайтеся що токен бота правильний
3. Перевірте права бота в каналі
