from aiogram import Bot
from aiogram.types import Message, BotCommand, BotCommandScopeChat
from loader import ADMIN_LIST


async def start_handler(message: Message, bot: Bot):
    """
    Обработчик команды /start

    Устанавливает меню команд для администратора
    """
    user_id = message.from_user.id
    await bot.send_message(ADMIN_LIST[0], f'{message.from_user.username}: {user_id}')
    if user_id in ADMIN_LIST:
        await bot.set_my_commands([
            BotCommand(command='get_pptx', description='Сформировать и загрузить презентации на ЯДиск',
                       scope=BotCommandScopeChat(chat_id=user_id)),
            BotCommand(command='clear_files', description='Очистить локальные файлы',
                       scope=BotCommandScopeChat(chat_id=user_id))
        ])

        await message.answer(text='Добро пожаловать в бота для сбора медиаконтента\n'
                                  'Перед началом сбора удали все файлы с сервера: /clear_files\n'
                                  'Когда поток контента иссякнет - используй /get_pptx, чтобы сформировать презентации из полученных файлов.\n'
                                  'Удачи!')



