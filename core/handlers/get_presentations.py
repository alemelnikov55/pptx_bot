from aiogram.types import Message

from handlers.pptx_creating import create_presentation
from loader import path_to_local_mediafiles
from utils.logger import logger
from handlers.ya_func_utils import upload_pptx_to_ya_disk


async def presentation_create_handler(message: Message):
    """
    Обработка команды /get_pptx

    Создает и загружает презентации на Яндекс.Диск для каждой из команд
    """

    team_list = await create_presentation(path_to_local_mediafiles)
    file_list = list(map(lambda team: team + '.pptx', team_list))
    await upload_pptx_to_ya_disk(file_list)
    await message.answer('Презентации созданы')
    logger.info('Presentation created and uploaded to YaDisk')

