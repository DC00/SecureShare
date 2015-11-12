from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    # app that controls the admin site. Go to the adminn site at localhost:8000/admin
    url(r'^admin/', include(admin.site.urls)),

    url(r'^reports/', include('secureshare.urls')),

    url(r'^contact/$', 'secureshare.views.contact', name='contact'),

    url(r'^about/$', 'secureshare.views.about', name='about'),

    url(r'^$', 'secureshare.views.home', name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

