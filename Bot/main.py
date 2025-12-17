import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from Bot.database.database import Data
from Bot.database.constants import API_TOKEN
from Bot.database.logger import logger
from Bot.handlers.handlers import router, handlers
# from Bot.handlers.callbacks import router_for_callbacks, callbacks

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
data = Data()

# Запуск проекта
if __name__ == '__main__':
    handlers(data)
    # callbacks(data)

    dp.include_router(router)
    # dp.include_router(router_for_callbacks)

    logger.info("Бот запущен")

    async def main():
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)


    asyncio.run(main())
