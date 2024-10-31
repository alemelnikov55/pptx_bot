## Collect pptx BOT ##

#### Описание ####
Бот обеспечивает сбор и обработку всех видео и фото материалов, присылаемых в чат, где находится бот.
Материалы собираются в локальном хранилище для их дальнейшего преобразования в презентацию. Помимо этого материалы отправляются на Яндекс.Диск для хранения и передачи клиенту.

Материалы от разных команд собираются в разные папки.
Структура папок на Яндекс.Диске:

- Корневая папка проекта
  - Папка ткущей даты в формате ДДММГГ
    - Папко команды 1
    - Папка команда ...
    - Папка команды N

#### Описание презентаций ####
Презентации формируются из присланных медиафалов. Все фото и видеоматериалы от команды формируются в презентацию последовательно, согласно времени отправки.
Перед слайдами с видео стоит слад-заглушка, где демонстрируется первый кадр из ролика
Соотношение сторон слайда - 16:9
Цвет фона слайдов - черный

#### Команды ####
***/get_pptx*** - Запускает процесс сборки презентаций и отправки их на Яндекс.Диск. По окончанию сборки бот присылает ответ: "Презентации созданы"
При повторном использовании данной команды формируется новые презнтации, отличить их можно будет по префиксу, котором указано время создания презентации
***/clear_storage*** - Очищает все файлы на сервере. Необходимо производить перед каждой игрой.