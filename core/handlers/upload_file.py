import shutil

from aiogram import Bot
from aiogram.types import Message

from utils.logger import logger
from handlers.ya_func_utils import upload_to_disk
from loader import path_to_local_mediafiles


# async def upload_video_handler(message: Message, bot: Bot):
#     """
#     Функция для обработки видеофайлов
#
#     Функция сохраняет поступивший файл в папку медиафалов проекта, формирует список файлов для отправки и передает его
#     для заливки на ЯДиск
#     """
#
#     chat_name = message.chat.title.replace(' ', '_')
#
#     if message.photo:
#         print('photo detected')
#         file_name = f'photo_{chat_name}_{message.photo[-1].file_unique_id}.jpg'
#         file = await bot.get_file(message.photo[-1].file_id)  # получение объекта file загруженного файла
#         shutil.copyfile(file.file_path,
#                         f'{path_to_local_mediafiles}/{file_name}')  # комируем файлы в папку медиафалов проекта
#         print('photo copyed')
#
#         video_list.append(f'{path_to_local_mediafiles}/{file_name}')
#
#     if message.video:
#         print('video detected')
#
#         file_name = f'video_{chat_name}_{message.video.file_unique_id}'
#         file_id = message.video.file_id  # Get file id
#         file = await bot.get_file(file_id)  # получение объекта file загруженного файла
#
#         file_extension = file.file_path.split('/')[-1].split('.')[-1]
#         shutil.copyfile(file.file_path, f'{path_to_local_mediafiles}/{file_name}.{file_extension}') # комируем файлы в папку медиафалов проекта
#         print('video copyed')
#
#         video_list.append(f'{path_to_local_mediafiles}/{file_name}.{file_extension}')
#
#     await upload_to_disk(video_list, chat_name)
#     print("video or photo uploaded")


async def upload_file_handler(message: Message, bot: Bot):
    """
    Функция для обработки видеофайлов

    Функция сохраняет поступивший файл в папку медиафалов проекта, формирует список файлов для отправки и передает его
    для заливки на ЯДиск
    """

    chat_name = message.chat.title.replace(' ', '_')

    if message.photo:
        logger.info('photo detected')
        file_name = f'photo_{chat_name}_{message.photo[-1].file_unique_id}.jpg'
        file = await bot.get_file(message.photo[-1].file_id)  # получение объекта file загруженного файла
        shutil.copyfile(file.file_path,
                        f'{path_to_local_mediafiles}/{file_name}')  # комируем файлы в папку медиафалов проекта
        logger.info('photo copyed')

        filepath = f'{path_to_local_mediafiles}/{file_name}'

    if message.video:
        logger.info('video detected')

        file_name = f'video_{chat_name}_{message.video.file_unique_id}'
        file_id = message.video.file_id  # Get file id
        file = await bot.get_file(file_id)  # получение объекта file загруженного файла

        file_extension = file.file_path.split('/')[-1].split('.')[-1]
        shutil.copyfile(file.file_path, f'{path_to_local_mediafiles}/{file_name}.{file_extension}') # копируем файлы в папку медиафалов проекта
        logger.info('video copyed')

        filepath = f'{path_to_local_mediafiles}/{file_name}.{file_extension}'

    await upload_to_disk(filepath, chat_name)
    logger.info(f"video or photo uploaded {filepath}")
