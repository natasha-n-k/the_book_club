from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True)

    def __str__(self):
        return self.user.username
    
class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200, default='None', null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='images')
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True)

    def __str__(self):
        return self.name

    def calculate_average_rating(self):
        return Rating.objects.filter(book=self).aggregate(Avg('rating'))['rating__avg']

class BookClub(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='images')
    venue = models.CharField(max_length=200, default='Online', null=True)
    members = models.ManyToManyField(User, related_name='clubs')
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='administered_clubs')
    selected_book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, related_name='selected_clubs')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    meeting = models.OneToOneField('Meeting', on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return self.name

class ClubPage(models.Model):
    book_club = models.ForeignKey(BookClub, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()

class UserBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    is_want_to_read = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    date_read = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, default='none')

    def __str__(self):
        return f"{self.user.username}'s {self.book.name}"


class Rating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_book = models.ForeignKey(UserBook, on_delete=models.CASCADE, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1)

    def __str__(self):
        return f"{self.user.username}'s rating for {self.book.name}"

    def save(self, *args, **kwargs):
        if not self.user_book:
            user_book, _ = UserBook.objects.get_or_create(user=self.user, book=self.book)
            self.user_book = user_book
        super().save(*args, **kwargs)

class BookPage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()

class Meeting(models.Model):
    date = models.DateField()
    location = models.CharField(max_length=100)

class Queue(models.Model):
    club = models.ForeignKey(BookClub, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Queue for {self.club.name}"