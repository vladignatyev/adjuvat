#!coding:utf-8
from crm.clients.forms import CreateClientForm
from crm.models import Client
from crm.views import need_company
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.six import text_type
from eztables.forms import DatatablesForm
from eztables.views import DatatablesView, RE_FORMATTED


@need_company
def update_view(request, client_id):
    try:
        client = Client.objects.get(pk=client_id, company=request.company)
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

@need_company
def new_client_view(request):
    new_client = Client()
    new_client.company = request.company

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


@need_company
def clients_list(request):
    return render_to_response('clients-list.html',
                              context_instance=RequestContext(request))


class ClientsDatatableView(DatatablesView):
    model = Client
    fields = (
        '{first_name} {last_name}',
        'phone',
        'sex',
        'birth_date',
        'mail'
    )

    display_fields = ('sex',)

    def get_company(self):
        return self.request.session.get('company', None)

    def global_search(self, queryset):
        return super(ClientsDatatableView, self).global_search(queryset).filter(company=self.get_company())

    def column_search(self, queryset):
        return super(ClientsDatatableView, self).column_search(queryset).filter(company=self.get_company())

    def get_queryset(self):
        return super(ClientsDatatableView, self).get_queryset().filter(company=self.get_company())

    def get_db_fields(self):
        if not self._db_fields:
            self._db_fields = []
            fields = self.fields.values() if isinstance(self.fields, dict) else self.fields
            for field in fields:
                if RE_FORMATTED.match(field):
                    self._db_fields.extend(RE_FORMATTED.findall(field))
                else:
                    self._db_fields.append(field)
        return self._db_fields

    def process_dt_response(self, data):
        self.form = DatatablesForm(data)
        if self.form.is_valid():
            # self.object_list = self.get_queryset().values(*self.get_db_fields())
            self.object_list = self.display_objects(self.get_queryset().all())
            return self.render_to_response(self.form)
        else:
            return HttpResponseBadRequest()

    def display_objects(self, objects):
        objects_list = []
        for object in objects:
            o = {}
            for field in self.get_db_fields():
                if field in self.display_fields:
                    o[field] = getattr(object, "get_%s_display" % field)()
                else:
                    o[field] = getattr(object, field)

            objects_list.append(o)
        return objects_list

    def get_row(self, row):
        '''Format a single row (if necessary)'''

        if isinstance(self.fields, dict):
            return dict([
                (key, text_type(value).format(**row) if RE_FORMATTED.match(value) else row[value])
                for key, value in self.fields.items()
            ])
        else:
            return [text_type(field).format(**row) if RE_FORMATTED.match(field)
                    else row[field]
                    for field in self.fields]


    def get_rows(self, rows):
        '''Format all rows'''
        return [self.get_row(row) for row in rows]