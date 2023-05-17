from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage(location='images')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField( null=True)

    def __str__(self):
        return self.user.username

class BookClub(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='images')
    venue = models.CharField(max_length=200, default='Online', null=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='clubs')

    def __str__(self):
        return self.name

class ClubPage(models.Model):
    book_club = models.ForeignKey(BookClub, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()

class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200, default='None', null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='images')
    is_want_to_read = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    date_read = models.DateField(blank=True, null=True)
    average_rating = models.DecimalField(max_digits=2, decimal_places=1, null=True)

    def __str__(self):
        return self.name

class Rating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))

    def __str__(self):
        return f"{self.user.username}'s rating for {self.book.name}"

class BookPage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()

