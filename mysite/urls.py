from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib import auth
from django.contrib import sites

urlpatterns = [
    # app that controls the admin site. Go to the adminn site at localhost:8000/admin
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'secureshare.views.home', name='home'),

    url(r'^reports/', include('secureshare.urls')),

]

