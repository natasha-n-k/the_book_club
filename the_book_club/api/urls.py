
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'bookclubs', views.BookClubViewSet)
router.register(r'books', views.BookViewSet)
router.register(r'userbooks', views.UserBookViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'ratings', views.RatingViewSet)
router.register(r'queues', views.QueueViewSet)
router.register(r'meetings', views.MeetingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
