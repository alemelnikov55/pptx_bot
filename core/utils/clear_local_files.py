import glob
import os

from loader import path_to_local_mediafiles


async def clear_local_mediafiles() -> None:
    """
    Удаляет все файлы в игровой директории.
    """
    files = glob.glob(f'{path_to_local_mediafiles}/*')
    for file in files:
        os.remove(file)
