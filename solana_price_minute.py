from dotenv import load_dotenv
import os
import requests
import pandas as pd
import asyncio
from datetime import datetime, timedelta, timezone


load_dotenv()


async def solana_price_minute(start_time, end_time):
    # Настройки API
    API_KEY = os.getenv("API_KEY")
    BASE_URL = "https://data.solanatracker.io/chart/So11111111111111111111111111111111111111112"  # Адрес SOL токена

    # массив, который возвращаем
    solana_history_json = []

    # Цикл для отрезков времени
    step = timedelta(minutes=900)  # Шаг в 900 минут (15 часов)
    current_time = start_time
    while current_time < end_time:
        next_time = current_time + step
        if next_time > end_time:
            next_time = end_time  # Гарантируем, что последний интервал не выходит за пределы

        time_from = int(current_time.timestamp())
        time_to = int((next_time - timedelta(minutes=1)).timestamp())
        current_time = next_time

        # Параметры запроса
        params = {
            "type": "1m",  # Интервал в 1 минуту
            "time_from": time_from,
            "time_to": time_to
        }

        # Выполняем запрос к API
        headers = {"x-api-key": API_KEY}
        response = requests.get(BASE_URL, params=params, headers=headers)

        # Проверка ответа
        if response.status_code == 200:
            data = response.json()
            solana_history_json.extend(data.get("oclhv", []))
            await asyncio.sleep(2)
        else:
            print("Ошибка:", response.status_code, response.text)
            return

    return solana_history_json
