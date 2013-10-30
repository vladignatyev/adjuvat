# Create your views here.
from crm.clients.forms import CreateClientForm
from crm.models import Company
from django.shortcuts import render_to_response
from django.template import RequestContext


def fake_auth(request):
    if not request.session.get('company', None):
        request.session['company'] = Company.objects.get(pk=1)


def dashboard_view(request):
    fake_auth(request)  # todo: remove and implement authorization
    return render_to_response('index.html', context_instance=RequestContext(request))
