# -*- coding: utf8 -*-

from django.forms import (ModelForm, Textarea, DateTimeInput, DateTimeField,
    HiddenInput, TimeField, TimeInput, ValidationError)
from django.conf import settings
from days_time import (getTeamDaysOff, checkIfDayOfWeekInDayOfWeekList,
    get_dinner_time)
from tickets.models import Ticket
from datetime import timedelta, date, time, datetime

common_fields_to_exclude = ('user_created', 'user_modified', 'date_created', 'date_modified')

class TicketForm(ModelForm):
    date_assigned = DateTimeField(label='Дата/Время', initial=date.today, widget=DateTimeInput(format=settings.FORMAT_DATE), input_formats=(settings.FORMAT_DATE,))
    time = TimeField(label='Длительность заявки', initial=time(hour=settings.DEFAULT_TIME), widget=TimeInput(format=settings.FORMAT_TIME), input_formats=(settings.FORMAT_TIME,))

    def __init__(self, *args, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs.pop('id')
        else:
            self.id = 0
        super(TicketForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(TicketForm, self).clean()

        if cleaned_data['team'].no_connection and cleaned_data['type'].pk == 1:
            raise ValidationError('Выбранная бригада не доступна для подлючения.')
        return cleaned_data

    def clean_date_assigned(self):
        def getTime(time):
            return timedelta(minutes=time.minute, hours=time.hour)

        def checkIfTimeIsFree(team, date_to_check_start, id, time):
            'Returns 0 if time is free'
            date_to_check_end = date_to_check_start + time

            def checkIfTimespanOverlaps(date1_start, date1_end, date2_start, date2_end):
                'date1 - date to check; date2 - date to compare with'
                if date1_start < date2_end and date1_end > date2_start:
                    return True

            def checkIfDayOff():
                days_off = getTeamDaysOff(team)
                return checkIfDayOfWeekInDayOfWeekList(date_to_check_start, days_off)

            def checkIfDinnerTime():
                dinner_time = get_dinner_time()
                current_date = date(year=date_to_check_start.year, month=date_to_check_start.month, day=date_to_check_start.day)
                dinner_start = datetime.combine(current_date, dinner_time[0])
                dinner_end = datetime.combine(current_date, dinner_time[1])
                return checkIfTimespanOverlaps(date_to_check_start, date_to_check_end, dinner_start, dinner_end)
            tickets = Ticket.objects.filter(team=team, status=1, date_assigned__year=date_to_check_start.year, date_assigned__month=date_to_check_start.month, date_assigned__day=date_to_check_start.day)
            if id:
                tickets = tickets.exclude(pk=id)
            for ticket in tickets:
                date_to_compare = ticket.date_assigned
                if checkIfTimespanOverlaps(date_to_check_start, date_to_check_end,
                                           date_to_compare, date_to_compare + timedelta(minutes=ticket.time.minute, hours=ticket.time.hour)):
                    return (0, ticket.id)
            if team.department.pk not in settings.TEAMS_NO_DINNER_NO_DAYS_OFF:
                if checkIfDayOff():
                    return (1, None)
                if checkIfDinnerTime():
                    return (2, None)
            return (-1, None)
        selected_date = self.cleaned_data['date_assigned']
        status, id = checkIfTimeIsFree(self.cleaned_data['team'], selected_date, self.id, getTime(self.cleaned_data['time']))
        if status != -1:
            if status == 0:
                error = 'Это время занято. (Заявка #%d).' % id
            elif status == 1:
                error = 'В этот день у бригады выходной.'
            elif status == 2:
                error = 'В это время у бригады обед.'
            raise ValidationError(error)
        return selected_date

    class Meta:
        textarea_settings = {'cols': 25, 'rows': 5}
        model = Ticket
        widgets = {
            'description': Textarea(attrs=textarea_settings),
            'solution': Textarea(attrs=textarea_settings),
            'status': HiddenInput,
        }


class EditTicketForm(TicketForm):
    class Meta(TicketForm.Meta):
        exclude = common_fields_to_exclude


class EditTicketSaveForm(TicketForm):
    class Meta(TicketForm.Meta):
        exclude = ('user_created', 'date_created', 'date_modified')


class AddTicketForm(TicketForm):
    class Meta(TicketForm.Meta):
        exclude = common_fields_to_exclude + ('solution', 'status', 'reason')


class AddTicketSaveForm(TicketForm):
    class Meta(TicketForm.Meta):
        exclude = ('date_created', 'date_modified', 'solution', 'status', 'reason')
