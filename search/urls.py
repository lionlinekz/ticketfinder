from django.conf.urls import patterns, url
from search import views

urlpatterns = patterns('',
		url(r'get_trains/', views.get_trains),
		url(r'places/', views.places),
		url(r'passenger/', views.passenger),
		url(r'buy_ticket/', views.buy_ticket),
		url(r'book/', views.book),
        url(r'^$', views.index, name='index'))