#Tickets

The web application on Python2/Django/jQuery. The ticket management system. 
It’s used by one of the local ISP companies in Russia. The interface is in Russian.

#Описание

Система позволяет добавлять, изменять, закрывать заявки, просматривать календарь заявок, формировать и печатать отчет о заявках на сегодня. Имеется фильтр заявок. При выборе диапазона даты, поле “дата” игнорируется. Права доступа: Пользователи могут добавлять заявки и вносить изменения. Администраторы могут закрывать заявки. Суперадминистраторы могут добавлять типы заявок и т. д.
    
##Installation instructions

* Insert your database settings and modify the variables in the following file:
    * /tickets_project/settings.py
* Run install.sh
* Modify the following files:
    * /templates/report_header.html
    * /static/js/settings.js
* Import db.sql to your database. db.sql also includes some example data.
