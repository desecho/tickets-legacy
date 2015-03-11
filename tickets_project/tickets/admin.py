from django.contrib import admin
from .models import (UserProfile, Department, Team, SubscriberType, Type,
                     Urgence, Ticket, Reason)


class TeamAdmin(admin.ModelAdmin):
    def queryset(self, request):
        qs = self.model.all.get_query_set()
        return qs


admin.site.register(UserProfile)
admin.site.register(Department)
admin.site.register(SubscriberType)
admin.site.register(Type)
admin.site.register(Team, TeamAdmin)
admin.site.register(Urgence)
admin.site.register(Ticket)
admin.site.register(Reason)
