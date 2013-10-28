from crm.clients.forms import CreateClientForm
from django.shortcuts import render_to_response
from django.template import RequestContext


def list_view(request):
    pass


def update_view(request):
    pass


def new_client_view(request):
    form = None
    if request.method == 'GET':
        form = CreateClientForm()
    else:
        form = CreateClientForm(request.POST)
    return render_to_response('new-user.html', {'form': form},
                              context_instance=RequestContext(request))