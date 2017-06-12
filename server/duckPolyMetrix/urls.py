from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index', views.index, name='index'),
    url(r'^changeProgram/(?P<program>\w+)/$', views.changeProgram, name='changeProgram'),
    url(r'^collapsibletree/(?P<matrix>\w+)/(?P<query>\w+)/$', views.collapsibletree, name='collapsibletree'),
    url(r'^zoomablesunburst/(?P<matrix>\w+)/(?P<query>\w+)/$', views.zoomablesunburst, name='zoomablesunburst'),
    url(r'^edgebundling/(?P<matrix>\w+)/(?P<query>\w+)/$', views.edgebundling, name='edgebundling'),
    url(r'^circlepacking/(?P<matrix>\w+)/(?P<query>\w+)/$', views.circlepacking, name='circlepacking'),
    url(r'^bubblechart/(?P<matrix>\w+)/(?P<query>\w+)/$', views.bubblechart, name='bubblechart'),
    url(r'^getResult/(?P<projectName>\w+)/$', views.getResult, name='getResult'),
    url(r'^parseProject/(?P<projectName>\w+)/$', views.parseProject, name='parseProject'),
    url(r'^uploadProjectJsonFile/$', views.uploadProjectJsonFile, name='uploadProjectJsonFile'),
    url(r'^detailQuery/$', views.detailQuery, name='detailQuery'),
]