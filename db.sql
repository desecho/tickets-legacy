insert  into `tickets_department`(`id`,`name`) values (1,'ОТП'),(2,'ОРС');
insert  into `tickets_reason`(`id`,`name`) values (1,'обрыв кабеля'),(2,'переобжим коннектора'),(3,'по вине абонента'),(4,'не отвечало оборудование'),(5,'абонента не было дома'),(6,'не обнаружено проблем');
insert  into `tickets_subscribertype`(`id`,`name`) values (1,'ФЛ'),(2,'ЮЛ'),(3,'Другой');
insert  into `tickets_team`(`id`,`name`,`department_id`,`days_off`) values (1,'Бригада 1',1,'1,7'),(2,'Бригада 2',1,'5,6');
insert  into `tickets_type`(`id`,`name`) values (1,'Подключение'),(2,'Развитие'),(3,'Ремонт');
insert  into `tickets_urgence`(`id`,`name`,`color`) values (1,'Низкая','green'),(2,'Нормальная','yellow'),(3,'Высокая','red');