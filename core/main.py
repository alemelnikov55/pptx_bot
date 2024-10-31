import asyncio
from aiogram import Dispatcher, F, Bot
from aiogram.filters import Command
from aiogram.client.telegram import TelegramAPIServer
from aiogram.client.session.aiohttp import AiohttpSession

from loader import TOKEN
from utils.logger import logger
from utils.support_commands import starting, stopping
from handlers.upload_file import upload_file_handler
from handlers.get_presentations import presentation_create_handler
from handlers.clear_local_storage_handler import clear_local_handlers, confirm_clear_server_kb_handler

# rsync -Praz /home/alex/PycharmProjects/vmeste_pro_bot/core alemel@194.87.187.251:/home/alemel/scout_bot/


async def start_bot() -> None:
    """
    Функция запуска бота
    """
    session = AiohttpSession(api=TelegramAPIServer.from_base('http://localhost:8081'))
    logger.info('Bot started at local telegram Bot API server')
    bot = Bot(token=TOKEN, parse_mode='HTML', session=session)
    dp = Dispatcher()
    dp.startup.register(starting)
    dp.shutdown.register(stopping)

    dp.callback_query.register(confirm_clear_server_kb_handler, F.data.startswith('clear_'))

    dp.message.register(presentation_create_handler, Command(commands='get_pptx'))
    dp.message.register(clear_local_handlers, Command(commands='clear_files'))

    # dp.message.register(upload_file_handler, F.photo)
    dp.message.register(upload_file_handler, F.video | F.photo)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start_bot())
