from django.urls import path
from django.conf import settings
from django.contrib import admin
from . import views

app_name = 'club'

urlpatterns = [
    path('', views.club, name='club'), 
]
