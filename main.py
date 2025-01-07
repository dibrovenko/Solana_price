import asyncio
from datetime import datetime, timedelta, timezone

from db.core import AsyncORM
from solana_price_minute import solana_price_minute
from visualize_solana_candlestick import visualize_solana_candlestick


async def main():
    # подключения к бд
    await AsyncORM.create_tables(flag='restart')

    # Определяем временные рамки (с 3 января по 7 января по Гринвичу)
    start_time = datetime(2025, 1, 3, 0, 0, 0, tzinfo=timezone.utc)  # Начало 3 января (UTC)
    end_time = datetime(2025, 1, 7, 0, 0, 0, tzinfo=timezone.utc)  # Конец 7 января (UTC)

    solana_history_json = await solana_price_minute(start_time=start_time, end_time=end_time)

    # Преобразуем данные и записываем в бд
    solana_history_sqlalchemy = []
    for solana_minute_json in solana_history_json:
        solana_minute_dto = AsyncORM.json_to_dto((solana_minute_json))
        solana_minute_sqlalchemy = AsyncORM.dto_to_sqlalchemy(solana_minute_dto)
        solana_history_sqlalchemy.append(solana_minute_sqlalchemy)

    await AsyncORM.insert_list_to_db(list_class_sqlalchemy=solana_history_sqlalchemy)

    # строим график
    visualize_solana_candlestick(data=solana_history_json)


# Запуск главной функции
if __name__ == "__main__":
    asyncio.run(main())