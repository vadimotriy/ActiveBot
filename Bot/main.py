import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from Bot.database.database import Data
from Bot.database.constants import API_TOKEN
from Bot.functions.logger import logger
from Bot.handlers.handlers import router, handlers
from Bot.handlers.callbacks import router_for_callbacks, callbacks
from Bot.handlers.admin import router_for_admin, admin

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
data = Data()

# Запуск проекта
if __name__ == "__main__":
    handlers(data)
    callbacks(data)
    admin(data, bot)

    dp.include_router(router)
    dp.include_router(router_for_callbacks)
    dp.include_router(router_for_admin)

    logger.info("Бот запущен")

    async def main():
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

    try:
        asyncio.run(main())
    except KeyboardInterrupt: # Остановка бота (Ctrl + C)
        logger.info("Бот выключен")