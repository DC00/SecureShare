from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render

from .models import Report

def index(request):
    latest_report_list = Report.objects.order_by('-created_at')
    
    # Loads the template at reports/index.html and passes it a context
    # the context is a dictionary mapping template variable names to Python objects
    # e.g. maps 'latest_report_list' -> latest_report_list
    context = {'latest_report_list': latest_report_list}
    return render(request, 'reports/index.html', context)

def detail(request, report_id):
    return HttpResponse("You're looking at report %s." % report_id)


