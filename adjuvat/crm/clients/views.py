#!coding:utf-8
from crm.clients.forms import CreateClientForm
from crm.models import Client
from django.contrib import messages
from django.core.urlresolvers import resolve, reverse
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template import RequestContext


def list_view(request):
    pass


def update_view(request, client_id):
    company = request.session.get('company', None)
    if not company:
        return HttpResponseForbidden()
    try:
        client = Client.objects.get(pk=client_id, company=company)
    except Client.DoesNotExist:
        return HttpResponseNotFound()

    if request.method == 'POST':
        form = CreateClientForm(request.POST, instance=client)
        try:
            existing_client = Client.objects.get(phone=form.instance.phone)
            if existing_client.id == client.id:
                raise Client.DoesNotExist()  # todo: holy fuck!
            messages.error(request,
                           u'Клиент с телефоном %s уже существует — %s!' % (
                               client.phone, _viewClientLink(existing_client)),
                           extra_tags='icon-exclamation-sign')
        except Client.DoesNotExist:
            # todo: extract the shit
            if form.is_valid():
                client.save(force_update=True)

                messages.success(request,
                                 u'Информация о клиенте обновлена!',
                                 extra_tags='icon-ok-sign')
    else:
        form = CreateClientForm(instance=client)

    return render_to_response('new-user.html',
                              {'form': form,
                               'update_mode': True},
                              context_instance=RequestContext(request))


def _viewClientLink(client):
    url = reverse('update_client_form', args=[client.id])
    return '<a href="%s">%s %s</a>' % (url, client.first_name, client.last_name,)


def new_client_view(request):
    company = request.session.get('company', None)
    if not company:
        return HttpResponseForbidden()

    new_client = Client()
    new_client.company = company

    if request.method == 'GET':
        form = CreateClientForm(instance=new_client, )
    else:
        form = CreateClientForm(request.POST, instance=new_client)

    if form.is_valid():
        try:
            existing_client = Client.objects.get(phone=new_client.phone)
            messages.error(request,
                           u'Клиент с телефоном %s уже существует — %s!' % (
                               new_client.phone, _viewClientLink(existing_client)),
                           extra_tags='icon-exclamation-sign')

        except Client.DoesNotExist:
            new_client.save()
            form = CreateClientForm()
            messages.success(request,
                             u'%s %s добавлен!' % (new_client.first_name, new_client.last_name),
                             extra_tags='icon-ok-sign')

    return render_to_response('new-user.html', {'form': form},
                              context_instance=RequestContext(request))