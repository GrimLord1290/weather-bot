import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import requests
import asyncio

load_dotenv()

# Токен и ключ берутся из .env
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Напиши город, и я скажу погоду.")

@dp.message()
async def weather(message: types.Message):
    city = message.text.strip()
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        await message.answer("Город не найден. Попробуй ещё раз.")
        return

    temp = data["main"]["temp"]
    feels = data["main"]["feels_like"]
    desc = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]

    text = (
        f"Погода в {city}:\n"
        f"🌡 Температура: {temp}°C\n"
        f"🤔 Ощущается как: {feels}°C\n"
        f"☁️ {desc.capitalize()}\n"
        f"💧 Влажность: {humidity}%"
    )
    await message.answer(text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
