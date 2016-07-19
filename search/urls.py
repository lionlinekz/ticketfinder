from django.conf.urls import patterns, url
from search import views

urlpatterns = patterns('',
		url(r'get_trains/', views.get_trains),
        url(r'^$', views.index, name='index'))