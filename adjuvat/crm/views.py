# Create your views here.
from crm.clients.forms import CreateClientForm
from crm.models import Company
from django.http import HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import RequestContext

# Decorator to provide current user company to all views
def need_company(viewfunc):
    def wrapped(request, *args):
        company = request.session.get('company', None)
        if not company:
            return HttpResponseForbidden()
        request.company = company
        return viewfunc(request, *args)

    return wrapped


def fake_auth(request):
    if not request.session.get('company', None):
        request.session['company'] = Company.objects.get(pk=1)


def dashboard_view(request):
    fake_auth(request)  # todo: remove and implement authorization
    return render_to_response('index.html', context_instance=RequestContext(request))
