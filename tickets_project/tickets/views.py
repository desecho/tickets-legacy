# -*- coding: utf8 -*-
import json
import copy

from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

from annoying.decorators import ajax_request, render_to
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.conf import settings

from .days_time import (getTeamDaysOff, checkIfDayOfWeekInDayOfWeekList,
                        get_dinner_time)
from .models import Ticket, Type, Team, Reason, ChangeLog
from .forms import (AddTicketSaveForm, AddTicketForm, EditTicketForm,
                    EditTicketSaveForm)


def logout_view(request):
    logout(request)
    return redirect('/login/')


@render_to('index.html')
@login_required
def home(request):
    filter_data = {'types': Type.objects.all(), 'teams': Team.objects.all(),
                   'reasons': Reason.objects.all()}
    filter = request.session.get('filter')
    # Filter open tickets by default
    if filter is None:
        filter = request.session['filter'] = {'status': 1}
        filter = request.session.get('filter')
    return {'filter_data': filter_data, 'filter': filter}


@render_to('calendar.html')
@login_required
def calendar(request):
    def processText(text):
        text = text.replace("'", '')
        text = ''.join(text.splitlines())
        return text

    def getYearMonthDay(date):
        output = {'year': date.year,
                  # -1 because months start from 0 in js
                  'month': date.month - 1,
                  'day': date.day}
        return output

    def getDateRange():
        def daterange(start_date, end_date):
            for n in range(int((end_date - start_date).days)):
                yield start_date + timedelta(n)
        start_date = date.today()
        end_date = start_date + relativedelta(
            months=settings.CALENDAR_DAYS_OFF_DISPLAY_MONTHS_AHEAD)
        return daterange(start_date, end_date)

    def getTeamsWithoutDinnerAndDaysOff():
        teams = Team.objects.all()
        for team_id in settings.TEAMS_NO_DINNER_NO_DAYS_OFF:
            teams = teams.exclude(department=team_id)
        return teams

    def joinDicts(x, y):
        return dict(x.items() + y.items())

    def getDinner():
        teams = getTeamsWithoutDinnerAndDaysOff()
        dates = []
        dinner_time = get_dinner_time()
        dinner_start = dinner_time[0]
        dinner_end = dinner_time[1]
        for team in teams:
            days_off = getTeamDaysOff(team)
            for date in getDateRange():
                if not checkIfDayOfWeekInDayOfWeekList(date, days_off):
                    dinner = {
                        'name': team.name,
                        'hour_start': dinner_start.hour,
                        'minute_start': dinner_start.minute,
                        'hour_end': dinner_end.hour,
                        'minute_end': dinner_end.minute,
                    }
                    dinner = joinDicts(dinner, getYearMonthDay(date))
                    dates.append(dinner)
        return dates

    def getDaysOff():
        teams = getTeamsWithoutDinnerAndDaysOff()
        dates = []
        for team in teams:
            days_off = getTeamDaysOff(team)
            for date in getDateRange():
                if checkIfDayOfWeekInDayOfWeekList(date, days_off):
                    day_off = {
                        'name': team.name,
                    }
                    day_off = joinDicts(day_off, getYearMonthDay(date))
                    dates.append(day_off)
        return dates

    def getTickets():
        tickets = Ticket.objects.filter(status=1).select_related()
        tickets_output = []
        for ticket in tickets:
            date_start = ticket.date_assigned
            date_end = ticket.date_assigned + timedelta(
                minutes=ticket.time.minute, hours=ticket.time.hour)
            title = '%s %s %s %s' % (
                ticket.type.name, ticket.team.name, ticket.subscriber_type.name,
                ticket.address)
            title = processText(title)
            description = processText(ticket.description)
            t = {
                'title': title,
                'year': date_start.year,
                # -1 because months start from 0 in js
                'month': date_start.month - 1,
                'day': date_start.day,
                'hour_start': date_start.hour,
                'minute_start': date_start.minute,
                'hour_end': date_end.hour,
                'minute_end': date_end.minute,
                'id': ticket.id,
                'description': description,
                'color': ticket.urgence.color
            }
            t = joinDicts(t, getYearMonthDay(date_start))
            tickets_output.append(t)
        return tickets_output
    tickets = getTickets()
    days_off = getDaysOff()
    dinners = getDinner()
    return {'tickets': tickets, 'days_off': days_off, 'dinners': dinners}


@render_to('report.html')
@login_required
def create_report(request, id):
    today = datetime.now()
    tickets = Ticket.objects.filter(status=1, date_assigned__year=today.year,
                                    date_assigned__month=today.month,
                                    date_assigned__day=today.day, team=id) \
                            .order_by('date_assigned')
    return {'tickets': tickets}


@render_to('report.html')
@login_required
def create_individual_report(request, id):
    tickets = Ticket.objects.filter(pk=id)
    return {'tickets': tickets}


def ajax_apply_filter(request):
    #assert False, request.session['filter']
    numeric_filters = ['status', 'team', 'type']
    if request.is_ajax() and request.method == 'POST':
        POST = request.POST
        if 'filter' in POST:
            filter = json.loads(POST.get('filter'))
            name = filter.keys()[0]
            value = filter[name]
            if name == 'clear':
                request.session['filter'] = {}
            else:
                if name in numeric_filters and value != '':
                    value = int(value)
                request.session['filter'] = request.session.get('filter', {})
                if value != '':
                    if name == 'date_range':
                            value = json.loads(value)
                            request.session['filter'][name] = {
                                'from': value['from'],
                                'to': value['to'],
                            }
                    else:
                        request.session['filter'][name] = value
                else:
                    if name in request.session['filter']:
                        request.session['filter'].pop(name)
    return HttpResponse()


def get_no_connection_team_ids_json():
    return json.dumps(list(
        Team.objects.filter(no_connection=True).values_list('pk', flat=True)))


@render_to('edit_ticket.html')
@login_required
def edit_ticket(request, id):
    def saveEditTicketForm(POST, FILES, ticket):
        POST = copy.copy(POST)
        POST['user_modified'] = request.user.pk

        # Logging changes if data has been changed
        old_date = ticket.date_assigned.strftime(settings.FORMAT_DATE)
        if POST['date_assigned'] != old_date:
            ChangeLog(ticket=ticket, user=request.user,
                      action='Date changed (%s -> %s)' % (old_date,
                      POST['date_assigned'].encode('UTF-8'))).save()
        form = EditTicketSaveForm(POST, FILES, instance=ticket, id=id)
        return saveForm(form)

    ticket = Ticket.objects.get(pk=id)
    message = None
    if request.method == 'POST':
        form = EditTicketForm(request.POST, request.FILES, id=id)
        if form.is_valid():
            if not form.cleaned_data['status']:
                if request.user.has_perm('tickets.can_change_ticket_status'):
                    if form.cleaned_data['solution']:
                        return saveEditTicketForm(request.POST, request.FILES,
                                                  ticket)
                    else:
                        message = {'message': 'Input Solution.',
                                   'error': False}
                else:
                    message = {'message': "You don't have permission to open ticket",
                               'error': True}
            else:
                return saveEditTicketForm(request.POST, request.FILES, ticket)
    else:
        form_initial_data = {
            'status': ticket.status,
            'type': ticket.type,
            'team': ticket.team,
            'subscriber_type': ticket.subscriber_type,
            'urgence': ticket.urgence,
            'account': ticket.account,
            'name': ticket.name,
            'address': ticket.address,
            'phone': ticket.phone,
            'price': ticket.price,
            'technical_data': ticket.technical_data,
            'date_assigned': ticket.date_assigned,
            'description': ticket.description,
            'time': ticket.time,
            'solution': ticket.solution,
            'reason': ticket.reason,
            'image': ticket.image,
        }
        form = EditTicketForm(initial=form_initial_data)
    return {'form': form, 'message': json.dumps(message),
            'submit_name': 'Save', 'ticket': ticket,
            'change_log': ticket.changelog_set.all(),
            'no_connection_team_ids': get_no_connection_team_ids_json()}


def saveForm(form):
    form.save()
    return HttpResponseRedirect(reverse('tickets.views.home'))


@render_to('edit_ticket.html')
@login_required
def add_ticket(request):
    if request.method == 'POST':
        form = AddTicketForm(request.POST)
        if form.is_valid():
            POST = copy.copy(request.POST)
            POST['user_created'] = request.user.pk
            POST['user_modified'] = request.user.pk
            form = AddTicketSaveForm(POST)
            return saveForm(form)
    else:
        form = AddTicketForm()
    return {'form': form, 'submit_name': 'Add',
            'no_connection_team_ids': get_no_connection_team_ids_json()}


@ajax_request
def ajax_get_ticket_list(request):
    def processEmptyFilters(filter):
        filter_output = copy.copy(filter)
        for f in filter:
            if filter.get(f) == '':
                filter_output.pop(f)
        return filter_output

    def convertToDatetime(date):
        return datetime.strptime(date, "%d.%m.%Y")

    def status_class_name(status, urgence_id):
        if status == 1:
            if urgence_id == 1:
                return 'priority-low'
            if urgence_id == 3:
                return 'priority-high'
        elif status == 2:
            return 'cancelled'
        else:
            return 'closed'

    if request.is_ajax() and request.method == 'GET':
        filter = request.session.get('filter')
        filter = processEmptyFilters(filter)
        if 'date_range' in filter:
            date_from = convertToDatetime(filter['date_range']['from'])
            date_to = convertToDatetime(filter['date_range']['to'])
            filter['date_assigned__range'] = (date_from, date_to)
            filter.pop('date_range')
            if 'date_assigned' in filter:
                filter.pop('date_assigned')
        else:
            if 'date_assigned' in filter:
                date_assigned = convertToDatetime(filter['date_assigned'])
                filter['date_assigned__year'] = date_assigned.strftime("%Y")
                filter['date_assigned__month'] = date_assigned.strftime("%m")
                filter['date_assigned__day'] = date_assigned.strftime("%d")
                filter.pop('date_assigned')
        if 'address' in filter:
            filter['address__icontains'] = filter['address']
            filter.pop('address')
        tickets = Ticket.objects.filter(**filter).select_related().values(
            'id', 'status', 'type__name', 'team__name', 'urgence__name',
            'subscriber_type__name', 'account', 'name', 'address', 'time',
            'date_assigned', 'urgence_id')
        tickets = tickets[:settings.TICKET_LISTING_LIMIT]
        tickets_output = []
        for ticket in tickets:
            commands = '''<a href="/edit-ticket/%d">Edit</a><br> |
                          <a href="/create-individual-report/%d">
                            Create task
                          </a>''' % (ticket['id'], ticket['id'])
            t = {
                '0': ticket['id'],
                '1': ticket['type__name'],
                '2': ticket['team__name'],
                '3': ticket['subscriber_type__name'],
                '4': ticket['account'],
                '5': ticket['name'],
                '6': ticket['address'],
                '7': ticket['time'].strftime("%H:%M"),
                '8': ticket['date_assigned'].strftime("%d.%m.%y %H:%M"),
                '9': commands,
                'DT_RowClass': status_class_name(ticket['status'],
                                                 ticket['urgence_id']),
            }
            tickets_output.append(t)
        output = {'data': tickets_output}
        return output
