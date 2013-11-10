from crm.clients.views import ClientsDatatableView
from django.conf.urls import patterns, url


urlpatterns = patterns('',
                       url(r'^dashboard/$', 'crm.views.dashboard_view', name='dashboard'),
                       url(r'^clients/new/$', 'crm.clients.views.new_client_view', name='new_client_form'),
                       url(r'^clients/list/$', 'crm.clients.views.clients_list', name='clients_list'),
                       url(r'^clients/update/(?P<client_id>\d+)/$', 'crm.clients.views.update_view',
                           name='update_client_form'),
                       url(r'^clients/list/ajax/', ClientsDatatableView.as_view(), name='clients_list_ajax')

                       )
