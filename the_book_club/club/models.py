from django.db import models
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage(location='media')

class BookClub(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='images')
    venue = models.CharField(max_length=200, default='Online', null=True)

    def __str__(self):
        return self.name

class ClubPage(models.Model):
    book_club = models.ForeignKey(BookClub, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()

class Book(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='images')

class BookPage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
