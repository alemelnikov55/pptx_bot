# import shutil
#
# from aiogram import Bot
# from aiogram.types import Message
#
# from handlers.ya_func_utils import upload_to_disk
# from loader import path_to_local_mediafiles
#
# photos_list = []
#
#
# async def upload_file_handler(message: Message, bot: Bot):
#     """
#     Функция для обработки фотографий
#
#     Функция сохраняет поступивший файл в папку медиафалов проекта, формирует список файлов для отправки и передает его
#     для заливки на ЯДиск
#     """
#     print('photo detected')
#     chat_name = message.chat.title.replace(' ', '_')
#
#     file_name = f'photo_{chat_name}_{message.photo[-1].file_unique_id}.jpg'
#     file = await bot.get_file(message.photo[-1].file_id) #  получение объекта file загруженного файла
#
#     shutil.copyfile(file.file_path, f'{path_to_local_mediafiles}/{file_name}') # комируем файлы в папку медиафалов проекта
#     print('photo copyed')
#
#     photos_list.append(file.file_path)
#     await upload_to_disk(photos_list, chat_name)
#     print('photo uploaded')
