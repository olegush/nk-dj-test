# nk-dj-test

## Запуск

1. Скачайте код

2. Установите Python 3 и зависимости из **requirements.txt**. Желательно использовать виртуальное окружение, например  с помощью библиотеки **venv**.

```bash
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt
```

3. Определите переменные окружения:
```bash
DEBUG=True
SECRET_KEY=django_secret_key
STATIC_URL=/static/
STATIC_ROOT=static
MEDIA_URL=/media/
MEDIA_ROOT=media
SITE=127.0.0.1
PG_USR=postgres_username
PG_PWD=postgres_password
PG_DB=postgres_database
EMAIL_HOST=smtp_server_for_emails
EMAIL_HOST_USER=email_from
EMAIL_PORT=smtp_port
EMAIL_HOST_PASSWORD=password
```

4. Создайте базу данных:
```bash
python3 manage.py migrate
```

5. Запустите сервер:
```bash
python3 manage.py runserver
```

6. Создайте администратора
```bash
python3 manage.py createsuperuser
```

7. Создайте стандартных пользователей и привязанных к ним авторов в админке http://127.0.0.1:8000/admin
