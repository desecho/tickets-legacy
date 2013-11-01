# -*- coding: utf8 -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.conf import settings

class Department(models.Model):
    name = models.CharField('название', max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'отдел'
        verbose_name_plural = 'отделы'


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    department = models.ForeignKey(Department, verbose_name='отдел')

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = 'профиль пользователя'
        verbose_name_plural = 'профили пользователей'


class Team(models.Model):
    name = models.CharField('название', max_length=255)
    department = models.ForeignKey(Department, verbose_name='отдел')
    days_off = models.CharField('выходные', max_length=255, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'бригада'
        verbose_name_plural = 'бригады'


class SubscriberType(models.Model):
    name = models.CharField('название', max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'тип абонента'
        verbose_name_plural = 'типы абонентов'


class Type(models.Model):
    name = models.CharField('название', max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'тип заявки'
        verbose_name_plural = 'типы заявок'

class Reason(models.Model):
    name = models.CharField('название', max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'причина'
        verbose_name_plural = 'причины'


class Urgence(models.Model):
    name = models.CharField('название', max_length=255)
    color = models.CharField('цвет', max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'срочность'
        verbose_name_plural = 'срочности'

class Ticket(models.Model):
    status = models.PositiveSmallIntegerField('статус', default=1)
    type = models.ForeignKey(Type, verbose_name='тип заявки')
    team = models.ForeignKey(Team, verbose_name='бригада')
    urgence = models.ForeignKey(Urgence, verbose_name='срочность', default=2)
    account = models.IntegerField('№ Договора', null=True, blank=True)
    name = models.CharField('ФИО', max_length=255)
    subscriber_type = models.ForeignKey(SubscriberType, verbose_name='тип абонента')
    price = models.CharField('стоимость подключения', null=True, blank=True, max_length=255)
    address = models.CharField('адрес', max_length=255)
    phone = models.CharField('телефон', max_length=255, null=True, blank=True)
    technical_data = models.CharField('тех. данные', max_length=255, null=True, blank=True)
    description = models.TextField('описание')
    solution = models.CharField('решение', max_length=255, null=True, blank=True)
    reason = models.ForeignKey(Reason, null=True, blank=True, verbose_name='причина')
    user_created = models.ForeignKey(User, related_name='ticket_created', verbose_name='пользователь добавивший')  # related name is used because of the clashing problem
    user_modified = models.ForeignKey(User, related_name='ticket_modified', verbose_name='пользователь изменивший')
    time = models.TimeField('длительность заявки', default=timedelta(minutes=60))
    date_assigned = models.DateTimeField('дата/время')
    date_created = models.DateTimeField('дата добавления', auto_now_add=True)
    date_modified = models.DateTimeField('дата изменения', auto_now=True)
    image = models.ImageField('изображение', upload_to=settings.UPLOAD_DIR, null=True, blank=True)

    class Meta:
        permissions = (
            ('can_change_ticket_status', 'Can change ticket status'),
        )
        verbose_name = 'заявка'
        verbose_name_plural = 'заявки'

    def __unicode__(self):
        return '%s - %s - %s' % (self.type.name, self.team.name, self.address)


class ChangeLog(models.Model):
    ticket = models.ForeignKey(Ticket, verbose_name='заявка')
    user = models.ForeignKey(User, verbose_name='пользователь изменивший')
    action = models.CharField('действие', max_length=255)
    date = models.DateTimeField('дата', auto_now_add=True)

    '''
    2DO
    def __unicode__(self):
        return self.action
    '''

    class Meta:
        verbose_name = 'лог изменений'
        verbose_name_plural = 'лог изменений'
