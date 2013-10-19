# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext


def dashboard_view(request):
    return render_to_response('index.html', context_instance=RequestContext(request))

def new_client_view(request):
    return render_to_response('new-user.html', context_instance=RequestContext(request))