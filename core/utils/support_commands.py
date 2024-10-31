from aiogram import Bot
from aiogram.types.bot_command_scope_chat import BotCommandScopeChat
from aiogram.types.bot_command import BotCommand

from loader import admin_id


async def set_commands(bot: Bot):
    """Функция для установки команд бота"""
    await bot.set_my_commands([
        BotCommand(command='get_pptx', description='Скачать презентацию',
                   scope=BotCommandScopeChat(chat_id=admin_id)),
        BotCommand(command='clear_files', description='Очистить локальные файлы',
                   scope=BotCommandScopeChat(chat_id=admin_id))
    ])


async def starting(bot: Bot) -> None:
    """Запуск бота """
    await set_commands(bot)
    await bot.send_message(admin_id, 'Бот запущен')


async def stopping(bot: Bot) -> None:
    """Остановка бота"""
    await bot.send_message(admin_id, 'Бот остановлен')
