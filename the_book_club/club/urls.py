from django.urls import path
from django.conf import settings
from django.contrib import admin
from . import views

app_name = 'club'

urlpatterns = [
    path('', views.index, name='index'), 
    path('book-clubs/', views.book_clubs, name='book_clubs'),
    path('books/', views.books, name='books'),
    path('<int:book_id>/', views.book_detail, name='book_detail'),
]
