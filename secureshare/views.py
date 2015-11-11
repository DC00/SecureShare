from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from django.conf import settings

from django.core.mail import send_mail

from .models import Report
from .forms import ContactForm, SignUpForm

# Views let you create objects that can then be used in the template
def home(request):
    title = "Welcome to SecureWitness"
    form = SignUpForm(request.POST or None)

    # if request.user.is_authenticated():
    #     title = "SecureWitness, Welcome %s" % (request.user)

    # Evetything in this dictionary can be used in templates/home.html
    # Add forms to context to use them in the view

    # print(request)
    # if request.method == "POST":
    #     print(request.POST)

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
        # print(instance.email)
        # print(instance.timestamp)
        context = {
            'title': "Thank you!",
        }

    return render(request, "home.html", context)

def index(request):
    latest_report_list = Report.objects.order_by('-created_at')
    
    # Loads the template at reports/index.html and passes it a context
    # the context is a dictionary mapping template variable names to Python objects
    # e.g. maps 'latest_report_list' -> latest_report_list
    context = {'latest_report_list': latest_report_list}
    return render(request, 'reports/index.html', context)

def detail(request, report_id):
    return HttpResponse("You're looking at report %s." % report_id)


    # This form lets you send messages with an email configured in settings.py
    # /contact/
def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        # iterate over fields
        # for key, value in form.cleaned_data.items():
        #     print(key, value)


        form_email = form.cleaned_data.get('email')
        form_message = form.cleaned_data.get("message")
        form_full_name = form.cleaned_data.get("full_name")
        # print(email, message, full_name)
        subject = 'Site contact form'
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email, 'yourotheremail@gmail.com']
        contact_message = "%s: %s via %s" % (form_full_name, 
            form_message, 
            form_email)

        send_mail(subject, 
            contact_message, 
            from_email, 
            to_email, 
            fail_silently=True)

    context = {
        'form': form,
    }
    return render(request, "forms.html", context)


