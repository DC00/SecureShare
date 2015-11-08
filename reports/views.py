from django.http import HttpResponse
from django.shortcuts import render
from .models import Report

def index(request):
    latest_report_list = Report.objects.order_by('-created_at')
    output = ""
    for r in latest_report_list.reverse():
        output += str(r.id) + " " + r.description + "<br>"
    # output = '<br>'.join([r.description for r in latest_report_list])
    return HttpResponse(output)

def detail(request, report_id):
    return HttpResponse("You're looking at report %s." % report_id)


