import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Токены из Railway
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши город, и я покажу погоду ☀️")


# Получение погоды
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        await update.message.reply_text("❌ Город не найден")
        return

    temp = data["main"]["temp"]
    description = data["weather"][0]["description"]

    await update.message.reply_text(
        f"🌆 Город: {city}\n🌡 Температура: {temp}°C\n☁️ Описание: {description}"
    )
    if __name__ == "__main__":
    print("Бот запущен...")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("weather", weather))

    app.run_polling()
