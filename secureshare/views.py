from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect

from .models import Report, Reporter, Message

from .forms import ReporterForm, MessageForm, ReportForm

# Views let you create objects that can then be used in the template
def home(request):
    title = "Welcome to SecureWitness"
    form = ReporterForm(request.POST or None)
    flag = False
    if request.user.is_authenticated():
        flag = True
        title = "SecureWitness, Welcome %s" % (request.user)

    #Evetything in this dictionary can be used in templates/home.html
    #Add forms to context to use them in the view

    print(request)
    if request.method == "POST":
        print(request.POST)

    context = {
        'title': title,
        'form': form,
        'flag': flag
    }

    if form.is_valid():

        # POST has a hash as well. Raw data. Don't do this
        # print(request.POST['email'])

        instance = form.save(commit=False)


        # commit=True
        instance.save()
        # print(instance.email)
        # print(instance.timestamp)
        context = {
            'title': "Thank you!",
        }

    return render(request, "home.html", context)

def index(request):
    latest_report_list = Report.objects.order_by('-created_at')
    form = ReportForm(request.POST or None)
    
    # Loads the template at reports/index.html and passes it a context
    # the context is a dictionary mapping template variable names to Python objects
    # e.g. maps 'latest_report_list' -> latest_report_list
    context = {'latest_report_list': latest_report_list, 
                'form' : form
                }
    if form.is_valid():

        # POST has a hash as well. Raw data. Don't do this
        # print(request.POST['email'])

        instance = form.save(commit=False)


        # commit=True
        instance.save()
        # print(instance.timestamp)
        context = {
            'title': "Thank you!",
    }
    return render(request, 'reports/index.html', context)

def windex(request):
    form = MessageForm(request.POST or None)
    
    latest_message_list = Message.objects.order_by('-created_at')
    title = 'my title'
    context = {
        'title': title,
        'latest_message_list' : latest_message_list,
        'form' : form,
    }

    if form.is_valid():

        # POST has a hash as well. Raw data. Don't do this
        # print(request.POST['email'])

        instance = form.save(commit=False)
        instance.reporter_it_belongs_to = request.user 
        print(instance.reporter_it_belongs_to)
        # commit=True
        instance.save()

        print(instance.content)
        print(instance.created_at)
        # print(instance.timestamp)
        context = {
            'title': "Thank you!",
        }

        # Loads the template at reports/index.html and passes it a context
    # the context is a dictionary mapping template variable names to Python objects
    # e.g. maps 'latest_report_list' -> latest_report_list
    
    return render(request, 'message/index2.html', context)

def sendmessage(request):
    form = MessageForm(request.POST or None)
    title = 'SEND NEW Message'
    context = {
        'title': title,
        'form': form
    }
    print('we were here')

    if form.is_valid():

        # POST has a hash as well. Raw data. Don't do this
        # print(request.POST['email'])

        instance = form.save(commit=False)
        instance.reporter_it_belongs_to = request.user 
        # commit=True
        instance.save()
        print('we were here')
        # print(instance.timestamp)
        context = {
            'title': "Thank you!",
        }
        return redirect('secureshare.views.sent')
        
    return render(request, 'sendmessage.html', context)

def createreport(request):
    form = ReportForm(request.POST or None)
    title = 'SEND NEW Message'
    context = {
        'title': title,
        'form': form
    }
    print('we were here')

    if form.is_valid():

        # POST has a hash as well. Raw data. Don't do this
        # print(request.POST['email'])

        instance = form.save(commit=False)
        # commit=True
        instance.save()
        print('we were here')
        # print(instance.timestamp)
        context = {
            'title': "Thank you!",
        }
        return redirect('secureshare.views.index')
        
    return render(request, 'reports/index.html', context)

def sent(request):
    return render(request, 'sent.html', [])

def detail(request, report_id):
    return HttpResponse("You're looking at report %s." % report_id)

def detail2(request, message_id):
    return HttpResponse("You're looking at message %s." % message_id)


def signup(request):
    form = ReporterForm(request.POST or None)

    title = 'HELLO, PLEASE SIGN UP!'
    #Evetything in this dictionary can be used in templates/home.html
    #Add forms to context to use them in the view

    context = {
        'title': title,
        'form': form
    }

    if form.is_valid():
        # POST has a hash as well. Raw data. Don't do this
        # print(request.POST['email'])

        instance = form.save(commit=False)


        # commit=True
        instance.save()
        print(instance.email)
        print(instance.last_name)

        context = {
            'title': "Thank you!",
        }
    
    return render(request, 'signup.html', context)




  
