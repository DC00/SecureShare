from django.conf.urls import url

from . import views

urlpatterns = [
    # /reports/
    url(r'^$', views.index, name='index'),

    url(r'^$', views.windex, name='windex'),

    # /reports/5/
    url(r'^(?P<report_id>[0-9]+)/$', views.detail, name='detail'),

    url(r'^(?P<message_id>[0-9]+)/$', views.detail2, name='detail2'),
]
