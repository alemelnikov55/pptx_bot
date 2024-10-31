from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from loader import admin_id
from utils.logger import logger
from utils.clear_local_files import clear_local_mediafiles


async def clear_local_handlers(message: Message) -> None:
    """
    Обработка команды /clear_files - только для администратора

    удаляет все файлы в игровой директории
    """
    kb = await confirm_clear_server_kb()
    if message.chat.type == 'private' and str(message.from_user.id) == admin_id:
        await message.answer('Вы уверены, что хотите удалить все медиафайлы с сервера?\n'
                             'Восстановить их не получится',
                             reply_markup=kb.as_markup())


async def confirm_clear_server_kb() -> InlineKeyboardBuilder:
    """
    Клавиатура для подтвреждения удаления локальных файлов
    """
    kb_builder = InlineKeyboardBuilder()
    kb_builder.add(InlineKeyboardButton(text='ДА', callback_data='clear_yes'))
    kb_builder.add(InlineKeyboardButton(text='НЕТ', callback_data='clear_no'))

    kb_builder.adjust(2)

    return kb_builder


async def confirm_clear_server_kb_handler(call: CallbackQuery) -> None:
    """
    Обработчик нажатия кнопок в меню подтверждения удаления

    :param call: CallbackQuery с данными о нажатой кнопке
    :return: None
    удаляет все медиафайлы с сервера при подтверждении, в противном случае отменяет удаление
    """
    _, confirm = call.data.split('_')
    if confirm == 'yes':
        await call.answer('Удаление медиафайлов началось...')
        try:
            await clear_local_mediafiles()
        except Exception as e:
            answers = str(e)
            await call.answer(answers)
        await call.message.answer("Сервер очищен успешно")
        logger.info("Сервер очищен успешно")

    elif confirm == 'no':
        await call.answer('Отмена')
        await call.message.answer('ну нет так нет')
