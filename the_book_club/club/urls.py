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
    path('append_to_queue/<int:book_id>/', views.append_to_queue, name='append_to_queue'),
    path('<int:club_id>/remove_from_queue/', views.remove_from_queue, name='remove_from_queue'),
    path('<int:club_id>/schedule_meeting/', views.schedule_meeting, name='schedule_meeting'),
    path('club/<int:club_id>/delete_meeting/<int:meeting_id>/', views.delete_meeting, name='delete_meeting'),
    path('create_club/', views.create_book_club, name='create_club'),
    path('comments/<int:book_id>/', views.comments, name='comments'),
]

