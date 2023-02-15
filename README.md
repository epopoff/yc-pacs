# All-in-one стенд облачного PACS

Стенд, имитирующий автооправку исследований в облачный PACS с локального.
Используется PACS Orthanc, использованы наработки из репозитория Osimis.

## Компоненты

![yc-pacs](https://user-images.githubusercontent.com/22369924/219082813-3c4eba42-5839-487c-abec-5c868c63051c.png)

- **pacs-db** - база данных в сервисе Managed PostgreSQL для хранения индексов
- **cloud-packs-bucket** - бакет в Object Storage для хранения DICOM файлов
- **traefik** - Traefik веб-сервер в роли reverse-proxy, автоматически генерирует SSL сертификаты
- **remote-pacs** - локальный PACS, автоотправка стабильных исследований в облако. БД файловая.
- **cloud-rw-pacs** - облачный PACS, прием исследований с удаленного. Запись в БД (Managed PostgreSQL) и Object Storage.
- **cloud-ro-pacs** - облачный PACS только для просмотра исследований. Чтение из БД и Object Storage.

## Бизнес-логика

<тут разместить схему бизнес-логики>

## Требуемые ресурсы Yandex Cloud

- Compute Cloud
- Managed PostgreSQL
- Object Storage
- VPC
- IAM

## Ссылки




## Благодарности
