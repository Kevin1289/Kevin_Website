from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path

from Train_Website.views import register, login_view, logout_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/$', register, name='register'),
    url(r'^login/$', login_view, name = 'login'),
    url(r'^logout/$', logout_view),
    path('', include('resume_page.urls')),
    path('admin/', admin.site.urls),
    path('', include('Train_Website.urls')),
]
