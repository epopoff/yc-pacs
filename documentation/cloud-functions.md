## whatsnew.py



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


