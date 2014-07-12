from datetime import time
from django.conf import settings


def getTeamDaysOff(team):
    days_off = team.days_off.split(',')
    days_off = [int(day) for day in days_off]
    return days_off


def checkIfDayOfWeekInDayOfWeekList(date, week_day_list):
    if date.isoweekday() in week_day_list:
        return True


def get_dinner_time():
    return (time(settings.DINNER_TIME[0]), time(settings.DINNER_TIME[1]))
