from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.home),
    path('add_password', views.add_password, name='add_password'),
    path('get_password', views.get_password, name='get_password'),
    path('change_password',views.change_password,name='change_password'),
    path('user_data', views.user_data, name='user_data'),
    path('coder_kira_12',views.coder_kira_12,name='coder_kira_12')
]


