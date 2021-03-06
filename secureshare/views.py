from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login
from django.utils import timezone

import base64
from encryption import encrypt, decrypt

from .search import *
from .indexer import *


from .encryption import encrypt, decrypt

from .models import Report, Reporter, Message, Group, Membership, Folder

from .forms import ReporterForm, MessageForm, ReportForm, ReportForm2, ReporterForm2, GroupForm, GroupForm2, FolderForm, FolderForm2

import os
BASE_DIR = os.getcwd()
MEDIA_DIR = "%s/media/" % (BASE_DIR)

# Views let you create objects that can then be used in the template
######################################################################
#BELOW IS THE HOME PAGE, LETS YOU SIGN UP OR LOG IN
######################################################################
def home(request):
    title = "Welcome to SecureWitness"
    flag = False
    is_super = False

    if request.user.is_authenticated():
        flag = True
        title = "SecureWitness, Welcome %s" % (request.user)
        logged_in_reporter = Reporter.objects.get(user_name=request.user)
        if logged_in_reporter.is_superuser:
            is_super = True

    #Evetything in this dictionary can be used in templates/home.html
    #Add forms to context to use them in the view

    print(request)
    if request.method == "POST":
        print(request.POST)

    context = {
        'title': title,
        'flag': flag,
        'is_super': is_super
    }
    return render(request, "home.html", context)
######################################################################
#BELOW ARE ALL OF THE PAGES THAT DISPLAY REPORTS,GROUPS,MESSAGES,ETC.
def index(request):
    # Want to display only the reports of the user that's logged in
    user_report_list = []
    user_made_report_list =[]
    user_made_folder_list =[]
    log = False
    if request.user.is_authenticated():
        log = True
        logged_in_reporter = Reporter.objects.get(user_name=request.user)

        if logged_in_reporter.is_superuser:
            user_report_list = Report.objects.all()
            for j in Report.objects.all():
                if j.reporter_it_belongs_to == logged_in_reporter:
                    user_made_report_list.append(j)

        else:
            for t in Report.objects.all():
                #if code breaks, take out this if series 
                if t.is_private == True:
                    pass
                    if t.reporter_it_belongs_to!=logged_in_reporter:                        
                        for r in t.reporters_that_can_view.all():
                            if r.user_name==logged_in_reporter.user_name:
                                user_report_list.append(t)

                        
                        for s in t.groups_that_can_view.all():
                            for u in s.members.all():
                                if u.user_name==logged_in_reporter.user_name:
                                    if t not in user_report_list:
                                        user_report_list.append(t)
                else: 
                    user_report_list.append(t)
                if t.reporter_it_belongs_to==logged_in_reporter: 
                    user_made_report_list.append(t) 

        for f in Folder.objects.all():
            print(f.owner)
            if f.owner == logged_in_reporter:
                user_made_folder_list.append(f)              

    # Loads the template at reports/index.html and passes it a context
    # the context is a dictionary mapping template variable names to Python objects
    # e.g. maps 'latest_report_list' -> latest_report_list
    context = {'user_report_list': user_report_list,
    'user_made_report_list': user_made_report_list,
    'user_made_folder_list': user_made_folder_list,
    'log' : log
            }
    
    return render(request, 'reports/index.html', context)




def windex(request):
    title = 'Welcome to Messages'
    log = False
    if request.user.is_authenticated():
        log = True
        latest_message_list = []
        logged_in_reporter = Reporter.objects.get(user_name=request.user)
        latest_message_list = Message.objects.all().filter(send_to=logged_in_reporter)
        #latest_message_list.sort(key=lambda x: x.created_at.lower())
        context = {
            'title': title,
            'latest_message_list' : latest_message_list,
            'log' : log

        }
    else:
        title = "please log in to see your messages"
        context = {
            'title': title,
            'log' : log
        }
    return render(request, 'message/index2.html', context)

def gindex(request):
    log = False
    if request.user.is_authenticated():
        log = True
        logged_in_reporter = Reporter.objects.get(user_name=request.user)
        latest_group_list = []

        if logged_in_reporter.is_superuser:
            latest_group_list = Group.objects.all()
        else:
            for g in Group.objects.all():
                for r in g.members.all():
                    if r == logged_in_reporter:
                        latest_group_list.append(g)

        title = 'Welcome to groups page'
        context = {
            'title': title,
            'latest_group_list' : latest_group_list,
            'log' : log
        }
    else: 
        title = "please log in to see your messages"
        context = {
            'title': title,
        }
    return render(request, 'gindex.html', context)
def rindex(request):
    log = False
    latest_reporter_list = Reporter.objects.order_by('user_name')
    if request.user.is_authenticated():
        log = True

    title = 'here are all reporters!'
    context = {
        'title': title,
        'latest_reporter_list' : latest_reporter_list,
        'log' : log
    }

        # Loads the template at reports/index.html and passes it a context
    # the context is a dictionary mapping template variable names to Python objects
    # e.g. maps 'latest_report_list' -> latest_report_list
    
    return render(request, 'rindex.html', context)
######################################################################
#BELOW IS RESPONSIBLE FOR ALL THE MESSAGE FUNCTIONALITY
######################################################################

def sendmessage(request):
    form = MessageForm(request.POST or None)
    title = 'SEND NEW Message'
    context = {
        'title': title,
        'form': form
    }

    if form.is_valid():

        # POST has a hash as well. Raw data. Don't do this
        # print(request.POST['email'])

        instance = form.save(commit=False)
        instance.sender = Reporter.objects.get(user_name=request.user)
        if instance.is_private == True:

            #print("sender password: %s " % (instance.send_to.password))
            #print("sending content: %s" % (instance.content))
            instance.content = base64.b64encode(encrypt(instance.content, instance.send_to.password))


        # commit=True
        instance.save()
        # print(instance.timestamp)
        context = {
            'title': "Thank you!",
        }
        return redirect('secureshare.views.sent')
        
    return render(request, 'sendmessage.html', context)
def decryptmessage(request, message_id):
    message = Message.objects.get(id=message_id)
    r_guy = Reporter.objects.get(user_name=request.user)
    #print("getter password: %s" % (r_guy.password))
    #print("message context, getter: %s" % (message.content))
    message.content = decrypt(base64.b64decode(message.content), r_guy.password)

    message.is_private = False
    message.save()
    context = {
        'Message' : message
    }

    return render(request, 'message.html', context)

def deletemessage(request, message_id):
    Message.objects.get(id=message_id).delete()
    return redirect('secureshare.views.windex')


######################################################################
#THE NAME PRETTY WELL DESCRIBES WHATS GOING ON HERE
######################################################################
def createreport(request):
    form = ReportForm(request.POST, request.FILES)
    
    title = 'Send New Report'
    context = {
        'title': title,
        'form': form
    }

    if form.is_valid():
        # POST has a hash as well. Raw data. Don't do this
        # print(request.POST['email'])
        if(request.FILES):
            r_thang = Report.objects.create(description=form.cleaned_data['description'], 
                                            full_description=form.cleaned_data['full_description'],
                                            is_private=form.cleaned_data['is_private'],
                                            uploaded_files=request.FILES['uploaded_files'])
        else:
            r_thang = Report.objects.create(description=form.cleaned_data['description'], 
                                            full_description=form.cleaned_data['full_description'],
                                            is_private=form.cleaned_data['is_private'])
        # for f in request.FILES:   
        #     r_thang.uploaded_files.add(f)
        # print (request.FILES['uploaded_files'])
        for u in form.cleaned_data['Select_Users']:
            r_thang.reporters_that_can_view.add(Reporter.objects.get(pk=u))
        for s in form.cleaned_data['Select_Groups']:
            r_thang.groups_that_can_view.add(Group.objects.get(pk=s))
        r_thang.reporter_it_belongs_to = Reporter.objects.get(user_name=request.user)
        # commit=True
        r_thang.save()
        # print(instance.timestamp)
        context = {
            'title': "Thank you!",
        }
        return redirect('secureshare.views.index')
        
    return render(request, 'createreport.html', context)

def editreport(request, report_id):

    my_record = Report.objects.get(id=report_id)
    form = ReportForm2(request.POST, request.FILES, instance=my_record)
    title = 'Send New Report'
    context = {
        'title': title,
        'form': form
    }
    if form.is_valid():

        # POST has a hash as well. Raw data. Don't do this
        # print(request.POST['email'])
        

        instance = form.save(commit=False)

        Report.objects.get(id=report_id).description = instance.description
        instance.save()
        Report.objects.get(id=report_id).full_description = instance.full_description

        # print(instance.timestamp)
        context = {
            'title': "Thank you!",
        }
        return redirect('secureshare.views.index')
    return render(request, 'editreport.html', context)

def deletereport(request, report_id):
    Report.objects.get(id=report_id).delete()
    return redirect('secureshare.views.index')
    
######################################################################
#DUHHHHHHHH
######################################################################
def creategroup(request):
    form = GroupForm(request.POST or None)
    title = 'Care to make a new group?'
    context = {
        'title': title,
        'form': form
    }

    if form.is_valid():

        # POST has a hash as well. Raw data. Don't do this
        # print(request.POST['email'])
        # commit=True
        g_thang = Group.objects.create(name=form.cleaned_data['name'])
        g_thang.save()
        for u in form.cleaned_data['Select_Users']:
            m_thang = Membership.objects.create(reporter=Reporter.objects.get(pk=u), group=g_thang)
            m_thang.save()
        #print(form.cleaned_data['Select_Users'])
        
        context = {
            'title': "Thank you!",
        }
        return redirect('secureshare.views.gindex')
    return render(request, 'creategroup.html', context)
def editgroup(request, group_id):
    group = Group.objects.get(pk=group_id)
    form = GroupForm2(request.POST or None)
    title = 'Add Group Members'
    context = {
        'title': title,
        'form': form
    }
    if form.is_valid():
        for u in form.cleaned_data['Select_Users']:
            if u not in group.members.all():
                #todo test adding memebrs 
                m_thang = Membership.objects.create(reporter=Reporter.objects.get(pk=u), group=group)
                m_thang.save()
            # POST has a hash as well. Raw data. Don't do this
        # print(request.POST['email'])
        

        

        # print(instance.timestamp)
        context = {
            'title': "Thank you!",
        }
        return redirect('secureshare.views.gindex')
    return render(request, 'editgroup.html', context)

######################################################################
#SERIOUSLY
######################################################################
def createfolder(request):
    form = FolderForm(request.POST or None)
    title = 'Care to make a new folder?'
    context = {
        'title': title,
        'form': form
    }

    if form.is_valid():

        # POST has a hash as well. Raw data. Don't do this
        # print(request.POST['email'])
        # commit=True
        f_thang = Folder.objects.create(name=form.cleaned_data['name'])
        f_thang.save()
        for u in form.cleaned_data['Select_Reports']:
            f_thang.contents.add(u)
        f_thang.owner = Reporter.objects.get(user_name=request.user)
        f_thang.save()  
        #print(form.cleaned_data['Select_Users'])

        context = {
            'title': "Thank you!",
        }
        return redirect('secureshare.views.index')
    return render(request, 'createfolder.html', context)

def editfolder(request, folder_id):

    my_record = Folder.objects.get(id=folder_id)
    form = FolderForm2(request.POST, instance=my_record)
    title = 'Edit Folder Name'
    context = {
        'title': title,
        'form': form
    }
    if form.is_valid():

        # POST has a hash as well. Raw data. Don't do this
        # print(request.POST['email'])
        

        instance = form.save(commit=False)
        instance.save()

        # print(instance.timestamp)
        context = {
            'title': "Thank you!",
        }
        return redirect('secureshare.views.index')
    return render(request, 'editfolder.html', context)

def deletefolder(request, folder_id):
    Folder.objects.get(id=folder_id).delete()
    return redirect('secureshare.views.index')
    
######################################################################
#SENT PAGES WON'T EARN YA POINTS,ONLY MADE ONE
def sent(request):
    return render(request, 'sent.html', [])
######################################################################
#DETAILS VIEWS ARE RESPONSIBLE FOR DISPLAY OF INVIDUAL REPORTS,MESSAGES,GROUPS,AND FOLDERS
def detail(request, report_id):
    report = Report.objects.get(id=report_id)

    logged_in_reporter = Reporter.objects.get(user_name=request.user)

    context = {
        'report' : report,
        'logged_in_reporter' : logged_in_reporter
    }


    return render(request, 'report.html', context)
    # return HttpResponse("You're looking at report %s." % report_id)

def detail2(request, message_id):
    message = Message.objects.get(id=message_id)
    context = {
        'Message' : message
    }

    return render(request, 'message.html', context)

def detail4(request, folder_id):
    folder = Folder.objects.get(id=folder_id)
    context = {
        'Folder' : folder
    }

    return render(request, 'folder.html', context)

def detail3(request, group_id):
    group = Group.objects.get(id=group_id)
    reporters = group.members.all()
    context = {
        'Group' : group,
        'Reporters' : reporters
    }
    return render(request, 'group.html', context)

def detail5(request, reporter_id):
    reporter = Reporter.objects.get(id=reporter_id)
    logged_in_reporter = Reporter.objects.get(user_name=request.user)

    flag = logged_in_reporter.is_superuser
    context = {
        'flag' : flag,
        'reporter' : reporter,
        'logged_in_reporter' : logged_in_reporter
    }
    return render(request, 'reporter.html', context)
######################################################################
#USER PROFILE STUFF
######################################################################
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
        user = User.objects.create_user(instance.user_name, instance.email, instance.password)
        instance.user = user
        # commit=True
        if not Reporter.objects.all():
            instance.is_superuser = True
        instance.save()

        context = {
            'title': "Thank you!",
        
        }
        return redirect('secureshare.views.home')
    return render(request, 'signin.html', context)


def signin(request):
    form = ReporterForm2(request.POST or None)

    title = 'HELLO, PLEASE SIGN IN'
    #Add forms to context to use them in the view

    context = {
        'title': title,
        'form': form
    }

    if form.is_valid():
        # POST has a hash as well. Raw data. Don't do this
        # print(request.POST['email'])

        instance = form.save(commit=False)
        user = authenticate(username=instance.user_name, password=instance.password)
        if user is not None:
        # the password verified for the user
            if user.is_active:
                login(request, user)
                return redirect('secureshare.views.index')
            else:
                title = "The password is valid, but the account has been disabled!"
                context = {
                    'title': title,
                    }
        
        else:
        # the authentication system was unable to verify the username and password
            title = "The username and password were incorrect."
            context = {
                'title': title,
                }
            
            

        
    
    return render(request, 'signin.html', context)

    def logout_view(request):
        logout(request)
        return render(request, 'home.html', [])


def makesuper(request, reporter_id):
    reporter = Reporter.objects.get(id=reporter_id)
    reporter.is_superuser = True
    reporter.save()
    context = {
        'reporter' : reporter,
    }

    return redirect('secureshare.views.rindex')
def suspend(request, reporter_id):
    reporter = Reporter.objects.get(id=reporter_id)
    reporter.user.is_active = False
    reporter.user.save()
    reporter.save()
    context = {
        'reporter' : reporter,
    }

    return redirect('secureshare.views.rindex')
def un_suspend(request, reporter_id):
    reporter = Reporter.objects.get(id=reporter_id)
    reporter.user.is_active = True
    reporter.user.save()
    reporter.save()
    context = {
        'reporter' : reporter,
    }

    return redirect('secureshare.views.rindex')
######################################################################
#THAT KID DANIEL'S STUFF
######################################################################
def download_report(request, report_id):
    report = Report.objects.get(id=report_id)
    make_downloadable_report(report, report_id)
    path_to_file = "static/downloadable_reports/report_%s.txt" % (report_id)
    f = open(path_to_file, 'r')
    response = HttpResponse(f, content_type='text/plain')
    response['Content-Disposition'] = "attachment; filename=report_%s.txt" % (report.id)
    return response

def make_downloadable_report(report, report_id):
    path_to_file = "static/downloadable_reports/report_%s.txt" % (report_id)
    fw = open(path_to_file, 'w')
    fw.write("Description: %s \n" % (report.description)) 
    fw.write("Full Description: %s \n" % (report.full_description)) 
    fw.write("Reporter: %s \n" % (report.reporter_it_belongs_to)) 

    filename = "%s" % (report.uploaded_files)
    path_to_file = "%s%s" % (MEDIA_DIR, filename[2:len(filename)])
    if not os.path.isfile(path_to_file):
        raise Exception, "file " + path_to_file + " not found."

    with open(path_to_file, 'rb') as f:
        text = f.read()
    f.closed

    fw.write("File: %s" % (text))

    fw.close()

def logout_view(request):
    logout(request)
    return render(request, 'home.html', [])

def view_file(request, filename):
    with open('media/%s' % (filename), 'r') as f:
        file_text = f.read().rstrip()

    context = {'file_text' : file_text}
    return render(request, 'view_file.html', context)



def search(request):
    if request.GET:
        make_search_index()
        query = request.GET['q']
        context = ranked_search(query)
        context['query'] = query
        return render(request, 'search.html', context)

    return render(request, 'search.html', {})




























  
