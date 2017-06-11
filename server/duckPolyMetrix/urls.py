from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index', views.index, name='index'),
    url(r'^getResult/(?P<projectName>\w+)/$', views.getResult, name='getResult'),
    url(r'^parseProject/(?P<projectName>\w+)/$', views.parseProject, name='parseProject'),
]