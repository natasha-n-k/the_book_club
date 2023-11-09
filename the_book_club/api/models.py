from django.db import models
from club.models import Book, BookClub, UserBook, Rating, Meeting, Queue, Comment
from django.contrib.auth.models import User

class APIProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True)

    def __str__(self):
        return self.user.username


class APIBook(models.Model):
    main_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='api_book')


class APIBookClub(models.Model):
    main_book_club = models.OneToOneField(BookClub, on_delete=models.CASCADE, related_name='api_book_club')


class APIUserBook(models.Model):
    main_user_book = models.OneToOneField(UserBook, on_delete=models.CASCADE, related_name='api_user_book')
