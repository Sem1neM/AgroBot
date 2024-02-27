import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import API_TOKEN
from handlers import router


# Обработчик события, выполняемого при запуске бота
# async def on_startup(dispatcher):
#     # Отправляем уведомление о запуске бота в администраторский чат
#     await bot.send_message(CHAT_ID, "Я родился.")
#
# async def on_shutdown(dispatcher):
#     # Отправляем уведомление об остановке бота в администраторский чат
#     await bot.send_message(CHAT_ID, "Я умер.")

# Функция для запуска бота
async def main():
    storage = MemoryStorage()
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(storage=storage)
    dp.include_router(router)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    await bot.delete_webhook(drop_pending_updates=True)

    # try:
    #     executor.start_polling(dp, skip_updates=True)
    #     # executor.start_polling(dp, skip_updates=True, on_shutdown=on_shutdown, on_startup=on_startup)
    # finally:
    #     asyncio.run(dp.storage.close())
    #     asyncio.run(dp.storage.wait_closed())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
