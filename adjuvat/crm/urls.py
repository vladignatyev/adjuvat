from django.conf.urls import patterns, url


urlpatterns = patterns('',
                       url(r'^dashboard/$', 'crm.views.dashboard_view', name='dashboard'),
                       url(r'^clients/new/$', 'crm.clients.views.new_client_view', name='new_client_form'),
                       )
