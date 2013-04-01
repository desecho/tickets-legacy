from tickets.models import UserProfile, Department, Team, SubscriberType, Type, Urgence, Ticket, Reason
from django.contrib import admin

admin.site.register(UserProfile)
admin.site.register(Department)
admin.site.register(SubscriberType)
admin.site.register(Type)
admin.site.register(Team)
admin.site.register(Urgence)
admin.site.register(Ticket)
admin.site.register(Reason)