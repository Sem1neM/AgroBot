import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import API_TOKEN, CHAT_ID
from handlers import router
from texts import STARTUP, SHUTDOWN

bot = Bot(token=API_TOKEN)

# Обработчик события, выполняемого при запуске бота
async def on_startup():
    # Отправляем уведомление о запуске бота в администраторский чат
    await bot.send_message(CHAT_ID, STARTUP)

# Обработчик события, выполняемого при отключении бота
async def on_shutdown():
    # Отправляем уведомление об остановке бота в администраторский чат
    await bot.send_message(CHAT_ID, SHUTDOWN)

# Функция для запуска бота
async def main():
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(router)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

    # Та же хрень, что и сверху, но с обработчиками событий включения и отключения
    # await executor.start_polling(bot, allowed_updates=dp.resolve_used_udpate_types, on_shutdown=on_shutdown,
    # on_startup=on_startup)
    await bot.delete_webhook(drop_pending_updates=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
