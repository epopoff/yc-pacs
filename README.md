Этот репозиторий содержит примеры развертывания PACS в Yandex Cloud.
Используется PACS Orthanc, использованы наработки из репозитория Osimis.

## Используемые сервисы Yandex Cloud

- [Compute Cloud ]() - виртуальные машины для развертывания Docker контейнеров
- [Managed Service for PostgreSQL]() - хранение индексов Orthanc
- [Object Storage]() - хранение DICOM файлов
- [Cloud Functions]() - python-функции с бизнес-логикой
- [Managed Service for YDB]() - база данных для бизнес-логики и сохранения состояний
- [Message Queue]() - очереди (можно заменить на Kafka в продуктовой среде)
- [Lockbox]() - хранение секретов
- [Virtual Private Cloud]() - сеть
- [Identity and Access Management]() - организация доступа (сервисные аккаунты)

## Структура проекта

- [dicom-examples]() - примеры DICOM файлов
- [documentation]() - документация по проекту, how-to
- [examples]() - примеры развертывания
- [python]() - скрипты бизнес-логики, полезные Jupyter ноутбуки
## Полезные ссылки

[Документация по Orthanc](https://book.orthanc-server.com/index.html)

[Rest API Orthanc](https://api.orthanc-server.com/)

[Репозиторий Osimis с примерами](https://github.com/orthanc-server/orthanc-setup-samples/tree/master)


## Благодарности
