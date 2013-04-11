#Tickets

The ticket managing system. It’s used by one of the local ISP companies in Russia.
The interface is in Russian.

#Описание

Система: Позволяет добавлять, изменять, закрывать заявки, просматривать календарь заявок, формировать и печатать отчет о заявках на сегодня. Имеется фильтр заявок. При выборе диапазона даты, поле “дата” игнорируется. Права доступа: Пользователи могут добавлять заявки и вносить изменения. Администраторы могут закрывать заявки. Суперадминистраторы могут добавлять типы заявок и т. д.

##Required packages

* [Python v2.6.5+](http://www.python.org)
* [Django v1.5.1](http://djangoproject.com)
* [django-annoying v0.7.7+](https://github.com/skorokithakis/django-annoying)
* [python-dateutil](ttp://labix.org/python-dateutil)
* [Python Imaging Library (PIL)](http://www.pythonware.com/products/pil/)
    * apt-get install python-imaging python-imaging-tk


##Used Javascript libraries
* [jQuery v1.9.1](http://jquery.com/)
* [jQuery UI v1.10.2](http://jqueryui.com/)
* [jQuery timepicker addon v1.2](http://trentrichardson.com/examples/timepicker/)
* [jQuery UI Bootstrap v0.5](http://addyosmani.github.com/jquery-ui-bootstrap/)
* [jQuery plugin: Validation v1.11.0](http://bassistance.de/jquery-plugins/jquery-plugin-validation/)
* [jGrowl v1.2.11]( https://github.com/stanlemon/jGrowl)
* [jQuery DataTables v1.9.4](http://www.datatables.net/)
* [FullCalendar v1.5.3](http://arshaw.com/fullcalendar/)
* [qTip2 v2.0.1](http://craigsworks.com/projects/qtip2/)
* [Bootstrap v2.3.1](http://twitter.github.com/bootstrap/)

##Installation instructions

* Insert your database settings and modify the variables in the following file:
    * /tickets_project/settings.py

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