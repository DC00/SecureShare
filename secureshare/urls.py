from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib import auth
from django.contrib import sites

from . import views

urlpatterns = [

	url(r'^admin/', include(admin.site.urls)),

	url(r'^$', 'secureshare.views.home', name='home'),




    url(r'^reports/$', views.index, name='reports'),
    
    url(r'^message/$', views.windex, name='message'),
    
    url(r'^groups/', views.gindex, name='groups'),


    url(r'^media/(?P<filename>.*)/$', views.view_file, name='detail'),




    
    url(r'^sendmessage/', views.sendmessage, name='sendmessage'),

    url(r'^creategroup/', views.creategroup, name='creategroup'),
    
    url(r'^createreport/', views.createreport, name='createreport'),

    url(r'^createfolder/', views.createfolder, name='createfolder'),




    url(r'^sent/', views.sent, name='sent'),



    
    url(r'^signup/', views.signup, name='signup'),
    url(r'^signin/', views.signin, name='signin'),
    url(r'^signout/', views.logout_view, name='logout_view'),



    #COO's shiz
    url(r'^reports/(?P<report_id>[0-9]+)/download$', views.download_report, name='detail'),


    # url(r'^reports/(?P<report_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^reports/(?P<report_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^message/(?P<message_id>[0-9]+)/$', views.detail2, name='detail2'),
    url(r'^group/(?P<group_id>[0-9]+)/$', views.detail3, name='detail3'),
    url(r'^folder/(?P<folder_id>[0-9]+)/$', views.detail4, name='detail4'),

    url(r'^deletereport/(?P<report_id>[0-9]+)/$', views.deletereport, name='deletereport'),
    url(r'^editreport/(?P<report_id>[0-9]+)/$', views.editreport, name='editreport'),

    url(r'^editfolder/(?P<folder_id>[0-9]+)/$', views.editfolder, name='editfolder'),
    url(r'^deletefolder/(?P<folder_id>[0-9]+)/$', views.deletefolder, name='deletefolder'),

]
