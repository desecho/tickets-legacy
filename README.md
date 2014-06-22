#Tickets

The ticket managing system. It’s used by one of the local ISP companies in Russia.
The interface is in Russian.

Uses Python 2, Django 1.5.

#Описание

Система: Позволяет добавлять, изменять, закрывать заявки, просматривать календарь заявок, формировать и печатать отчет о заявках на сегодня. Имеется фильтр заявок. При выборе диапазона даты, поле “дата” игнорируется. Права доступа: Пользователи могут добавлять заявки и вносить изменения. Администраторы могут закрывать заявки. Суперадминистраторы могут добавлять типы заявок и т. д.
    
##Installation instructions

* Insert your database settings and modify the variables in the following file:
    * /tickets_project/settings.py

* Run install.sh

* Modify the following files:
    * /templates/report_header.html
    * /static/js/settings.js

* Run
```
python manage.py syncdb
python manage.py collectstatic
python manage.py shell
```

* Import db.sql to your database. db.sql also includes some example data.