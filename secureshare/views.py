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




from .models import Report, Reporter, Message, Group, Membership, Folder

from .forms import ReporterForm, MessageForm, ReportForm, ReportForm2, ReporterForm2, GroupForm, FolderForm, FolderForm2

# Views let you create objects that can then be used in the template
######################################################################
#BELOW IS THE HOME PAGE, LETS YOU SIGN UP OR LOG IN
######################################################################
def home(request):
    title = "Welcome to SecureWitness"
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
        'flag': flag
    }
    return render(request, "home.html", context)
######################################################################
#BELOW ARE ALL OF THE PAGES THAT DISPLAY REPORTS,GROUPS,MESSAGES,ETC.
def index(request):
    # Want to display only the reports of the user that's logged in
    user_report_list = []
    user_made_report_list =[]
    user_made_folder_list =[]    
    if request.user.is_authenticated():
        logged_in_reporter = Reporter.objects.get(user_name=request.user)
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
    'user_made_folder_list': user_made_folder_list
            }
    
    return render(request, 'reports/index.html', context)




def windex(request):
    title = 'Welcome to Messages'

    latest_message_list = []
    if request.user.is_authenticated():
        logged_in_reporter = Reporter.objects.get(user_name=request.user)
        latest_message_list = Message.objects.all().filter(send_to=logged_in_reporter)
        #latest_message_list.sort(key=lambda x: x.created_at.lower())
    context = {
        'title': title,
        'latest_message_list' : latest_message_list,
    }

    return render(request, 'message/index2.html', context)

def gindex(request):
    
    latest_group_list = Group.objects.order_by('name')
    title = 'hey you made it to groups!'
    context = {
        'title': title,
        'latest_group_list' : latest_group_list,
    }


        # Loads the template at reports/index.html and passes it a context
    # the context is a dictionary mapping template variable names to Python objects
    # e.g. maps 'latest_report_list' -> latest_report_list
    
    return render(request, 'gindex.html', context)
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
        # commit=True
        instance.save()
        print('we were here')
        # print(instance.timestamp)
        context = {
            'title': "Thank you!",
        }
        return redirect('secureshare.views.sent')
        
    return render(request, 'sendmessage.html', context)



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
        print('here')
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

        print(instance.description)
        Report.objects.get(id=report_id).description = instance.description
        instance.save()
        print(Report.objects.get(id=report_id).description)
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
    print(folder.name)
    context = {
        'Folder' : folder
    }

    return render(request, 'folder.html', context)

def detail3(request, group_id):
    return render(request, 'gindex.html', context)
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
        instance.save()
        print(instance.email)

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
                print("The password is valid, but the account has been disabled!")
        else:
        # the authentication system was unable to verify the username and password
            print("The username and password were incorrect.")
            return redirect('secureshare.views.signin')
        

        context = {
            'title': "Thank you!",
        }
    
    return render(request, 'signin.html', context)

    def logout_view(request):
        logout(request)
        return render(request, 'home.html', [])
######################################################################
#THAT KID DAVID'S STUFF
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
    fw.close()

def logout_view(request):
    logout(request)
    return render(request, 'home.html', [])

  
