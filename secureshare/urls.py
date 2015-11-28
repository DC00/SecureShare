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
    
    url(r'^message/', views.windex, name='message'),
    
    url(r'^groups/', views.gindex, name='groups'),




    
    url(r'^sendmessage/', views.sendmessage, name='sendmessage'),

    url(r'^creategroup/', views.creategroup, name='creategroup'),
    
    url(r'^createreport/', views.createreport, name='createreport'),




    url(r'^sent/', views.sent, name='sent'),



    
    url(r'^signup/', views.signup, name='signup'),
    url(r'^signin/', views.signin, name='signin'),
    url(r'^signout/', views.logout_view, name='logout_view'),




    # /reports/5/
    # url(r'^reports/(?P<report_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^reports/(?P<report_id>[0-9]+)/$', views.detail, name='detail'),


    url(r'^message/(?P<message_id>[0-9]+)/$', views.detail2, name='detail2'),
]
