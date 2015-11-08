from django.conf.urls import url

from . import views

urlpatterns = [
    # /reports/
    url(r'^$', views.index, name='index'),

    # /reports/5/
    url(r'^(?P<report_id>[0-9]+)/$', views.detail, name='detail'),
]
