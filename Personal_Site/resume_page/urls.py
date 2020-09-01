from django.urls import include, path
from .import views


urlpatterns = [
    path('', views.home_page, name="homepage"),
    path('Train_project', views.train_project, name='train_project'),
    path('iFeeder', views.iFeeder, name='iFeeder'),
    path('ifeeder_ppt', views.ifeeder_ppt, name='ifeeder_ppt'),
    path('ifeeder_flowchart', views.ifeeder_flowchart, name='ifeeder_flowchart'),
    path('ifeeder_ad', views.ifeeder_ad, name='ifeeder_ad'),
]
