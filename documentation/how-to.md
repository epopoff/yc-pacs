## SSH
**Создать SSH ключ**:
```shell
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

**Добавить SSH-ключ в SSH-агент**:
1. Запустить ssh-agent:
```shell
eval "$(ssh-agent -s)"
```
2. Изменить `~/.ssh/config` чтобы автоматически загружать ключи в ssh-agent и сохранять парольные фразы в вашей связке ключей:
```
Host github.com
  AddKeysToAgent yes
  UseKeychain yes
  IdentityFile ~/.ssh/id_rsa
```
4. Добавьте свой закрытый ключ SSH в ssh-agent и сохраните свою кодовую фразу в связке ключей:
```shell
ssh-add --apple-use-keychain ~/.ssh/id_rsa
```

**Скопировать ssh-ключ**:
```shell
pbcopy < ~/.ssh/id_rsa.pub
```

## Готовим Docker





## Готовим облако

**Требуемые ресурсы**
- Compute Cloud
- VPC
- IAM
- Managed PostgreSQL
- Object Storage

**Дополнительно понадобится**
- домен, привязанный к Cloud DNS

### Создать сервисный аккаунт
Имя: **cloud-pacs-sa**
Роли:
- viewer
- storage.uploader
- storage.editor
- ~~serverless.functions.invoker~~
- monitoring.editor


### Создать кластер PostgreSQL
1. Имя кластера: **pg-cluster**
2. Окружение: PRESTABLE
3. Тип: **s3-c2-m8**
4. Размер хранилища: **network-ssd**
5. База данных:
	1. Имя: **pacs-db**
	2. Имя пользователя: **pacs-db-user**
	3. Пароль: **ваш пароль**
6. Установить плагин  `pg_trgm`


### Создать бакет Object Storage
1. Имя: **cloud-pacs-bucket**
2. Ограничение на размер: **500 ГБ**
3. Получить статический ключ доступа и сохранить себе идентификатор ключа и ключ

### Создать ВМ
1. Имя: **cloud-pacs-vm**
2. Операционная система: **Ubuntu 22.04**
3. Диск: **50ГБ**
4. vCPU: **2**
5. Гарантированная доля vCPU: **20%**
6. RAM: **2ГБ**
7. Выбрать сервисный аккаунт
8. Добавить имя пользователя и публичный ключ SSH

### Добавить DNS записи
1. **cloud-pacs-vm** - чтобы удобнее подключаться к ВМ
2. **yc-traefik** - веб-интерфейс *Traefik*
3. **remote-pacs** - веб-интерфейс *Remote PACS*
4. **cloud-rw-pacs** - веб-интерфейс *Cloud Read-Write PACS*
5. **cloud-ro-pacs** - веб-интерфейс *Cloud Read-only PACS*


## Подготовка ВМ
**Обновить пакеты**
```
sudo apt update && sudo apt upgrade -y
```

**Установить Docker**
[Установить Docker](https://docs.docker.com/engine/install/ubuntu/)
[Linux post-installation steps for Docker Engine](https://docs.docker.com/engine/install/linux-postinstall/)

Сгенерировать пароль в base64 для Traefik, используя `htpasswd`
```
htpasswd -nb admin admin_strong_password_102938
```
