import shutil

from aiogram import Bot
from aiogram.types import Message

from utils.logger import logger
from handlers.ya_func_utils import upload_to_disk
from loader import path_to_local_mediafiles
from pathlib import PurePath, PosixPath


async def upload_file_handler(message: Message, bot: Bot):
    """
    Функция для обработки видеофайлов

    Функция сохраняет поступивший файл в папку медиафалов проекта, формирует список файлов для отправки и передает его
    для заливки на ЯДиск
    """
    chat_name = message.chat.title.replace(' ', '_')

    if message.photo:
        logger.info('photo detected')

        file_name = PurePath(f'photo_{chat_name}_{message.photo[-1].file_unique_id}.jpg')
        source_file = await bot.get_file(message.photo[-1].file_id)  # получение объекта file загруженного файла
        filepath = PurePath(path_to_local_mediafiles, file_name)

        shutil.copyfile(source_file.file_path, filepath)
        logger.info('photo copyed')

    if message.video:
        logger.info('video detected')

        file_id = message.video.file_id  # Get file id
        source_file = await bot.get_file(file_id)  # получение объекта file загруженного файла

        source_file = PurePath(source_file.file_path)
        file_name = PosixPath(f'video_{chat_name}_{message.video.file_unique_id}').with_suffix(PurePath(source_file).suffix)
        filepath = PosixPath(path_to_local_mediafiles, file_name)

        shutil.copyfile(source_file.as_posix(), filepath.as_posix()) # копируем файлы в папку медиафалов проекта
        logger.info('video copyed')
    await upload_to_disk(filepath, chat_name)
    logger.info(f"video or photo uploaded {filepath}")
