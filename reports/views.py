from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("You're at the SecureWitness index.")

def detail(request, report_id):
    return HttpResponse("You're looking at report %s." % report_id)
