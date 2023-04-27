from django.db import models

class BookClub(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    language = models.CharField(max_length=2)

class ClubPage(models.Model):
    book_club = models.ForeignKey(BookClub, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    language = models.CharField(max_length=2)