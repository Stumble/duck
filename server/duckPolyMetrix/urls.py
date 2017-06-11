from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index', views.index, name='index'),
    url(r'^collapsibletree/(?P<metrix>\w+)/(?P<query>\w+)/$', views.collapsibletree, name='collapsibletree'),
    url(r'^zoomablesunburst/(?P<matrix>\w+)/(?P<query>\w+)/$', views.zoomablesunburst, name='zoomablesunburst'),
    url(r'^edgebundling/(?P<matrix>\w+)/(?P<query>\w+)/$', views.edgebundling, name='edgebundling'),
    url(r'^circlepacking/(?P<matrix>\w+)/(?P<query>\w+)/$', views.circlepacking, name='circlepacking'),
    url(r'^getResult/(?P<projectName>\w+)/$', views.getResult, name='getResult'),
    url(r'^parseProject/(?P<projectName>\w+)/$', views.parseProject, name='parseProject'),
]
