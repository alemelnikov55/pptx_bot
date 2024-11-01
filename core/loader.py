import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

if not find_dotenv():
    exit('Файл .env не найден. Переменные не загружены')
else:
    load_dotenv()

path_to_local_mediafiles = Path('.', 'mediafiles').absolute()
# path_to_local_files = '/home/alex/bin/7058585368:AAEd3hKCh71DF23GBdShZzzU2D9dudzDSeQ/videos/'

TOKEN = os.getenv('TOKEN')
admin_id = os.getenv('admin_id')
ya_disk_token = os.getenv('ya_disk_token')
project_folder = os.getenv('project_folder')
