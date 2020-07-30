from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from . import views
from .views import test

urlpatterns = [
    url(r'^test/$', views.test),
    path('Train_Choose_Service', views.Train_Choose_Service, name='Train_Choose_Service'),
    url(r'^all_stops/$', views.all_stops, name='all_stops'),
    url(r'^common_stations/$', views.common_stations, name='common_stations'),
    path('history', views.History, name='history'),
    path('logout', views.logout_view, name='logout'),
]
