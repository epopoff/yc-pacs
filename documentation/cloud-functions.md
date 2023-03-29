## whatsnew.py

![yc-pacs-whatsnew py](https://user-images.githubusercontent.com/22369924/228567505-cf0cc5b4-b1ed-41bd-ab1d-cf03637bdf62.png)

Функция запускается по расписанию и проверяет наличие новых исследований в remote-pacs.
Информацию о новых исследованиях функция записывает в YDB и идентификаторы в YMQ для дальнейшего перемещения в cloud-rw-pacs.

**Переменные окружения:**
- DOCAPI_ENDPOINT - эндпоинт для подключения к документным таблицам YDB
- YMQ_ENDPOINT - эндпоинт для подключения к YMQ
- REMOTE_PACS_ENDPOINT - эндпоинт для обращения к REST API remote-pacs

**Секреты Lockbox:**
- ACCESS_KEY_ID - идентификатор статического ключа доступа
- SECRET_ACCESS_KEY - ключ статического ключа доступа
- REMOTE_PACS_USER - имя пользователя для авторизации на remote-pacs
- REMOTE_PACS_PASSWORD - пароль для авторизации на remote-pacs

## transfer.py

![yc-pacs-transfer py](https://user-images.githubusercontent.com/22369924/228567577-c101e568-86b5-411a-927f-eee98d60d7cb.png)

Функция запускается по триггеру и сообщает cloud-rw-pacs, что нужно забрать исследования с remote-pacs.

**Переменные окружения:**
- DOCAPI_ENDPOINT - эндпоинт для подключения к документным таблицам YDB
- YMQ_ENDPOINT - эндпоинт для подключения к YMQ
- CLOUD_RW_PACS_ENDPOINT - эндпоинт для обращения к REST API cloud-rw-pacs

**Секреты Lockbox:**
- ACCESS_KEY_ID - идентификатор статического ключа доступа
- SECRET_ACCESS_KEY - ключ статического ключа доступа
- CLOUD_RW_PACS_USER - имя пользователя для авторизации на cloud-rw-pacs
- CLOUD_RW_PACS_PASSWORD - пароль для авторизации на cloud-rw-pacs

## clear-remote.py

![yc-pacs-clear-remote py](https://user-images.githubusercontent.com/22369924/228567717-ad6894d2-2e24-4dac-af72-fde8624d2d6e.png)

Функция запускается по таймеру и удаляет из remote-pacs все исследования, успешно перемещенные в cloud-rw-pacs.
Проверка осуществляется по двум параметрам:
- количество инстансов
- занимаемый объем

**Переменные окружения:**
- DOCAPI_ENDPOINT - эндпоинт для подключения к документным таблицам YDB
- CLOUD_RW_PACS_ENDPOINT - эндпоинт для обращения к REST API cloud-rw-pacs
- REMOTE_PACS_ENDPOINT - эндпоинт для обращения к REST API remote-pacs

**Секреты Lockbox:**
- ACCESS_KEY_ID - идентификатор статического ключа доступа
- SECRET_ACCESS_KEY - ключ статического ключа доступа
- CLOUD_RW_PACS_USER - имя пользователя для авторизации на cloud-rw-pacs
- CLOUD_RW_PACS_PASSWORD - пароль для авторизации на cloud-rw-pacs
- REMOTE_PACS_USER - имя пользователя для авторизации на remote-pacs
- REMOTE_PACS_PASSWORD - пароль для авторизации на remote-pacs
