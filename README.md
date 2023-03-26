# All-in-one стенд облачного PACS

Стенд, имитирующий автооправку исследований в облачный PACS с локального.
Используется PACS Orthanc, использованы наработки из репозитория Osimis.

## Компоненты

![yc-pacs-architecture](https://user-images.githubusercontent.com/22369924/227762026-fb50d351-a331-47c7-9ce2-5a07682aa396.png)

**Compute Cloud VM**
- **traefik** - Traefik веб-сервер в роли reverse-proxy, автоматически генерирует SSL сертификаты
- **remote-pacs** - имитация локального PACS, автоотправка стабильных исследований в облако. БД файловая.
- **cloud-rw-pacs** - облачный PACS, прием исследований с удаленного. Запись в БД (Managed PostgreSQL) и Object Storage.
- **cloud-ro-pacs** - облачный PACS только для просмотра исследований. Чтение из БД и Object Storage.

**pg-cluster:**
- **pacs-db** - база данных в сервисе Managed PostgreSQL для хранения индексов

**Object Storage:**
- **cloud-packs-bucket** - бакет в Object Storage для хранения DICOM файлов
- **studies-bucket** - бакет в Object Storage для хранения архивов исследований

**Cloud Functions:**
- **whatsnew.py** - функция проверки новых исследований на remote-pacs
- **transfer.py** - функция перемещения новых исследований с remote-pacs на cloud-pacs

**YDB:**
- **studies** - таблица в БД для хранения информации об исследованиях
- **studies** - таблица в БД для хранения индексов последних прочитанных изменений

**YMQ:**
**new-studies** - очередь с идентификаторами новых исследований в remote-pacs


## Бизнес-логика

![yc-pacs-TO-BE](https://user-images.githubusercontent.com/22369924/227762411-3f47466d-bbf6-410d-92b2-0d6b050d0ee0.png)

красным выделены еще не реализованные элементы

[Описание работы бизнес-логики]()

## Требуемые ресурсы Yandex Cloud

- Compute Cloud
- Managed Service for PostgreSQL
- Object Storage
- Managed Service for YDB
- Message Queue
- Cloud Functions
- Lockbox
- Virtual Private Cloud
- Identity and Access Management

## Ссылки

[Документация по Orthanc](https://book.orthanc-server.com/index.html)

[Rest API Orthanc](https://api.orthanc-server.com/)

[Репозиторий Osimis с примерами](https://bitbucket.org/osimis/orthanc-setup-samples/src/master/)


## Благодарности
