from pathlib import Path
import datetime
import yadisk
import yadisk.settings

from utils.logger import logger
from loader import project_folder, path_to_local_mediafiles, ya_disk_token

Path(path_to_local_mediafiles).mkdir(parents=True, exist_ok=True)
# client = yadisk.AsyncClient(token=ya_disk_token, )

# yadisk.settings.DEFAULT_UPLOAD_RETRY_INTERVAL = 5
# yadisk.settings.DEFAULT_RETRY_INTERVAL = 5
#
# print(yadisk.settings.DEFAULT_UPLOAD_TIMEOUT,
#       yadisk.settings.DEFAULT_TIMEOUT,
#       yadisk.settings.DEFAULT_UPLOAD_RETRY_INTERVAL,
#       yadisk.settings.DEFAULT_N_RETRIES,
#       yadisk.settings.DEFAULT_RETRY_INTERVAL)


async def create_team_folder(team_name: str):
    """
    Создает папку для команды на ЯндексДиске

    :param team_name: str имя команды
    :return: None
    """
    folder_name = team_name.replace(' ', '_').replace('/', '')
    date = datetime.date.strftime(datetime.date.today(), "%d%m%y")
    async with yadisk.AsyncClient(token=ya_disk_token, session="aiohttp") as client:
        if not await client.exists(f"{project_folder}/{date}/{folder_name}/"):
            logger.info('NonExisting path')
            try:
                await client.mkdir(f"{project_folder}/{date}")
            except yadisk.exceptions.DirectoryExistsError:
                logger.warning('Directory already exists')
            await client.mkdir(f"{project_folder}/{date}/{folder_name}")


# async def upload_to_disk(list_of_files: list, chat_name: str):
#     """
#     Загрузка медиафалов на ЯДиск
#
#     :param list_of_files: list[str] список имен файлов
#     :param chat_name: str имя чата или команды
#     :return: None
#     Сохораняет полученные от команды медиафайлы в папку команды
#     """
#     date = datetime.date.strftime(datetime.date.today(), "%d%m%y")
#     folder_name = chat_name.replace(' ', '_').replace('/', '')
#     destination_path = f'{project_folder}/{date}/{folder_name}'
#
#     async with yadisk.AsyncClient(token=ya_disk_token, session="aiohttp") as client:
#         if not await client.exists(destination_path):
#             await create_team_folder(folder_name)
#             print(f"New folder created {destination_path}")
#
#     for file in list_of_files:
#         print(file)
#         id_for_delete = list_of_files.index(file)
#         list_of_files.pop(id_for_delete)
#         try:
#             try:
#                 await fast_video_upload(file, destination_path)
#             except yadisk.exceptions.ParentNotFoundError as error:
#                 print(error)
#
#         except yadisk.exceptions.PathExistsError as error:
#             print(error)
#
async def upload_to_disk(file: str, chat_name: str):
    """
    Загрузка медиафалов на ЯДиск

    :param file: str путь дофайла
    :param chat_name: str имя чата или команды
    :return: None
    Проверяет, есть ли папка для команды. Если нет - создает папку по названию чата
    Сохораняет полученные от команды медиафайлы в папку команды
    """
    date = datetime.date.strftime(datetime.date.today(), "%d%m%y")
    folder_name = chat_name.replace(' ', '_').replace('/', '')
    destination_path = f'{project_folder}/{date}/{folder_name}'

    async with yadisk.AsyncClient(token=ya_disk_token, session="aiohttp") as client:
        if not await client.exists(destination_path):
            await create_team_folder(folder_name)
            logger.warning(f"New folder created {destination_path}")
        try:
            await fast_file_upload(file, destination_path)
        except (yadisk.exceptions.ParentNotFoundError, yadisk.exceptions.PathExistsError) as error:
            logger.error(error)


async def fast_file_upload(source_path: str, full_destination_path: str):
    """
    Функция для загрузки файлов

    :param source_path: str путь к исходному видеофайлу
    :param full_destination_path: str полный путь к конечной папке на ЯДиске

    Функция определяет тип файла.
    Для видео: Функция обрезает раширение файла, чтобы обойти ограничение по скорости для видеофайлов.
    А затем меняет расширение файла уже в облаке.
    Для остальный типов файлов - стандартное копирование на ЯДиск
    ОГРАНИЧЕНИЕЯ: в названии файла не должно быть точек '.'
    """
    file_type = source_path.split('/')[-1].split('.')[-1]
    async with yadisk.AsyncClient(token=ya_disk_token, session="aiohttp") as client:
        if file_type.lower() in ('mp4', 'mov'):
            modify_file_name = source_path.split('/')[-1].split('.')[0]  # обрезка расширения
            full_destination_path = full_destination_path + '/' + modify_file_name

            await client.upload(source_path, full_destination_path)# загрузка видео файла без ограничений по скорости

            # переименование файла в конечной папке
            correct_file_name = modify_file_name + '.' + file_type  # правильное имя файла с расширением
            await client.rename(full_destination_path, correct_file_name)  # изменение расширения на ЯДиске
            return
        # Загрузка остальных типов файлов
        file_name = source_path.split('/')[-1]
        await client.upload(source_path, f"{full_destination_path}/{file_name}")


async def upload_pptx_to_ya_disk(list_of_files: list):
    """
    Загрузка списка презентаций на Яндекс Диск

    :param list_of_files: list[str] список имен файлов
    :return: None
    """
    date = datetime.date.strftime(datetime.date.today(), "%d%m%y")
    async with yadisk.AsyncClient(token=ya_disk_token, session="aiohttp") as client:
        for file in list_of_files:
            try:
                await client.upload(f"{path_to_local_mediafiles}/{file}",
                                    f"{project_folder}/{date}/{file}")
            except yadisk.exceptions.ParentNotFoundError:
                await create_team_folder('')
                await client.upload(f"{path_to_local_mediafiles}/{file}",
                                    f"{project_folder}/{date}/{file}")
                logger.warning(f"New folder created {project_folder}/{date}/{file}")

            # logger.info(f"uploading takes {datetime.datetime.now() - start_time} seconds")
