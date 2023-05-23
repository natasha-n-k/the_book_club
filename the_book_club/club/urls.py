from django.urls import path
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

app_name = 'club'

urlpatterns = [
    path('', views.index, name='index'), 
    path('book-clubs/', views.book_clubs, name='book_clubs'),
    path('books/', views.books, name='books'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('club/<int:club_id>/', views.club_detail, name='club_detail'),
    path('accounts/profile/', views.account, name='account'),
    path('login/', auth_views.LoginView.as_view(template_name='club/login.html'), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'), 
    path('join_club/<int:club_id>/', views.join_club, name='join_club'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('update_book_status/<int:book_id>/<str:status>/', views.update_book_status, name='update_book_status'),
    path('book/<int:book_id>/rate/', views.rate_book, name='rate_book'),
    path('club/<int:club_id>/select_book/', views.select_book, name='select_book'),
    path('club/<int:club_id>/mark_book_read/', views.mark_book_read, name='mark_book_read'),
    path('<int:club_id>/admin/', views.club_admin, name='club_admin'),
    path('<int:club_id>/add_to_queue/', views.add_to_queue, name='add_to_queue'),
]
