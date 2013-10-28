# Create your views here.
from crm.clients.forms import CreateClientForm
from django.shortcuts import render_to_response
from django.template import RequestContext


def dashboard_view(request):
    return render_to_response('index.html', context_instance=RequestContext(request))

