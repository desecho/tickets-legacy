from django.contrib import admin
from .models import (UserProfile, Department, Team, SubscriberType, Type,
                     Urgence, Ticket, Reason)

admin.site.register(UserProfile)
admin.site.register(Department)
admin.site.register(SubscriberType)
admin.site.register(Type)
admin.site.register(Team)
admin.site.register(Urgence)
admin.site.register(Ticket)
admin.site.register(Reason)
