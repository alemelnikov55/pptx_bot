from pathlib import Path, PosixPath
import datetime
import yadisk
import yadisk.settings

from utils.logger import logger
from loader import project_folder, path_to_local_mediafiles, ya_disk_token

Path(path_to_local_mediafiles).mkdir(parents=True, exist_ok=True)


async def create_team_folder(team_name: str):
    """
    Создает папку для команды на ЯндексДиске

    :param team_name: str имя команды
    :return: None
    """
    folder_name = team_name.replace(' ', '_').replace('/', '')
    date = datetime.date.strftime(datetime.date.today(), "%d%m%y")
    destination_folder_on_yadisk = Path(project_folder, date, folder_name)

    async with yadisk.AsyncClient(token=ya_disk_token, session="aiohttp") as client:
        if not await client.exists(destination_folder_on_yadisk.as_posix()):
            logger.info('NonExisting path')

            try:
                await client.mkdir(destination_folder_on_yadisk.parent.as_posix())
            except yadisk.exceptions.DirectoryExistsError:
                logger.warning('Directory already exists')
            await client.mkdir(destination_folder_on_yadisk.as_posix())


async def upload_to_disk(file: PosixPath, chat_name: str):
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
    destination_path = Path('', project_folder, date, folder_name)

    async with yadisk.AsyncClient(token=ya_disk_token, session="aiohttp") as client:
        if not await client.exists(destination_path.as_posix()):
            await create_team_folder(folder_name)
            logger.warning(f"New folder created {destination_path}")
        try:
            await fast_file_upload(file, destination_path)
        except (yadisk.exceptions.ParentNotFoundError, yadisk.exceptions.PathExistsError) as error:
            logger.error(error)


async def fast_file_upload(source_path: Path, full_destination_path: Path):
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
    file_extension = source_path.suffix

    async with yadisk.AsyncClient(token=ya_disk_token, session="aiohttp") as client:
        if file_extension.lower() in ('mp4', 'mov'):
            modify_file_name = source_path.stem  # обрезка расширения
            full_destination_path = Path(full_destination_path, modify_file_name)

            await client.upload(source_path.as_posix(), full_destination_path)# загрузка видео файла без ограничений по скорости

            # переименование файла в конечной папке
            await client.rename(full_destination_path, full_destination_path.with_suffix(file_extension))  # изменение расширения на ЯДиске
            return
        # Загрузка остальных типов файлов
        file_name = source_path.name
        try:
            await client.upload(source_path.as_posix(), PosixPath(full_destination_path, file_name).as_posix())
        except yadisk.exceptions.RequestTimeoutError as e:
            logger.error(f'{file_name} file handeling error: {e}')


async def upload_pptx_to_ya_disk(list_of_files: list):
    """
    Загрузка списка презентаций на Яндекс Диск

    :param list_of_files: list[str] список имен файлов
    :return: None
    """
    date = datetime.date.strftime(datetime.date.today(), "%d%m%y")
    async with yadisk.AsyncClient(token=ya_disk_token, session="aiohttp") as client:
        for file in list_of_files:

            full_destination_path = Path(project_folder, date, file).as_posix()
            source_path = Path(path_to_local_mediafiles, file).absolute().as_posix()

            try:
                await client.upload(source_path, full_destination_path)
            except yadisk.exceptions.ParentNotFoundError:

                try:
                    await create_team_folder('')
                except yadisk.exceptions.DirectoryExistsError as e:
                    logger.error(e)

                await client.upload(source_path, full_destination_path)
                logger.warning(f"New folder created {full_destination_path}")
