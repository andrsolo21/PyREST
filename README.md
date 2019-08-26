# PyREST
opening a project in school backend development

## Инструкция по установке

### Настройка базы данных

Необходимо создать пользователя и базу данных, дать право пользователю на полное редактирование БД.
А также назначить пользователя на создание баз данных.

В проекте использовалась СУБД Postgres.

В настройках проекта указаны
* пользователь - shop_user_2
* пароль - mypassword
* база данных - shop_db_2

При желании можно поменять пользователя, пароль, бд и субд, только это необходимо описать в начтройках проекта.
Файл settings.py.

### Установка необходимого ПО

Все необходимые библиотеки описаны в файле requirements.txt, их необходимо установить.

А также должен быть установлен Nginx.
### Развертывание платформы

Для развертывания сервиса нелбходимо создать виртуальное окружение.

Далее из гита подтягивается репозиторий с проектом.

https://github.com/andrsolo21/PyREST

В настройках проекта в листе ALLOWED_HOSTS необходимо дописать свой ip или домен. 

На этом этапе уже можно запустить сервис:

python mysite/manage.py runserver 0.0.0.0:8080

### Миграции

Вызываем 2 команды:

python mysite/manage.py makemigrations

python mysite/manage.py migrate

### Настройка gunicorn

открываем файл

sudo vim /etc/systemd/system/gunicorn.service

Вставляем:

[Unit] 
Description=gunicorn daemon 
After=network.target 

[Service] 
User=entrant 
Group=www-data 
WorkingDirectory=/home/entrant/code/PyREST 
ExecStart=/home/entrant/code/PyREST/env/bin/gunicorn —access-logfile - —workers 8 —bind unix:/home/entrant/code/PyREST/mysite.sock mysite.wsgi:application 

[Install] 
WantedBy=multi-user.target 

запускаем:

sudo systemctl start gunicorn
sudo systemctl enable gunicorn

### Настройка Nginx

открываем:

sudo vim /etc/nginx/sites-available/mysite

вставляем:

server { 
listen 80; 
server_name 84.201.161.199; 

location = /favicon.ico { access_log off; log_not_found off; } 
location /static/ { 
root /home/entrant/code/PyREST/mysite; 
} 

location / { 
include proxy_params; 
proxy_pass http://unix:/home/entrant/code/PyREST/mysite/mysite.sock; 
} 
}

далее

sudo ln -s /etc/nginx/sites-available/mysite /etc/nginx/sites-enabled

sudo systemctl restart nginx

sudo ufw allow 'Nginx Full'

DONE)))))))

## Запуск тестов

python mysite/manage.py test tests.test_reqest




