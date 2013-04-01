from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'tickets.views.home'),
    url(r'^add-ticket/$', 'tickets.views.add_ticket'),
    url(r'^create-report/(?P<id>\d+)?$', 'tickets.views.create_report'),
    url(r'^edit-ticket/(?P<id>\d+)$', 'tickets.views.edit_ticket'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^logout/$', 'tickets.views.logout_view'),
    url(r'^get-ticket-list/$', 'tickets.views.ajax_get_ticket_list'),
    url(r'^apply-filter/$', 'tickets.views.ajax_apply_filter'),
    url(r'^calendar/$', 'tickets.views.calendar'),
    # url(r'^create-pdf/$', 'tickets.views.ajax_create_pdf'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
