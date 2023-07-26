from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True)

    def __str__(self):
        return self.user.username
    
class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200, default='None', null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='images', null=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    genre = models.CharField(max_length=100, null=True)
    theme = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

    def calculate_average_rating(self):
        return Rating.objects.filter(book=self).aggregate(Avg('rating'))['rating__avg']

class BookClub(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='images', null=True)
    venue = models.CharField(max_length=200, default='Online', null=True)
    members = models.ManyToManyField(User, related_name='clubs')
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='administered_clubs')
    selected_book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, related_name='selected_clubs')
    read_books = models.ManyToManyField(Book, related_name='read_clubs')
    book_queue = models.ManyToManyField(Book, through='Queue', related_name='queued_clubs')
    book_queue_members = models.ManyToManyField(User, through='Queue', related_name='queued_books')
    genre = models.CharField(max_length=100, null=True)
    theme = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

class UserBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    is_want_to_read = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    date_read = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, default='none')

    def __str__(self):
        return f"{self.user.username}'s {self.book.name}"

    def save(self, *args, **kwargs):
        # When saving the UserBook, update the book status and date_read fields
        if self.status == 'read' and not self.date_read:
            self.date_read = date.today()
        elif self.status != 'read':
            self.date_read = None
        super().save(*args, **kwargs)


class Rating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    user_book = models.ForeignKey(UserBook, on_delete=models.CASCADE, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1)

    def __str__(self):
        return f"{self.user.username}'s rating for {self.book.name}"

    def save(self, *args, **kwargs):
        if not self.user_book:
            user_book, _ = UserBook.objects.get_or_create(user=self.user, book=self.book)
            self.user_book = user_book
        super().save(*args, **kwargs)
        

class Meeting(models.Model):
    date = models.DateField()
    location = models.CharField(max_length=100)
    location_link = models.URLField(null=True, blank=True)
    club = models.ManyToManyField(BookClub, related_name='meetings')

    def __str__(self):
        club_names = ", ".join([club.name for club in self.club.all()])
        return f"Meeting for {club_names}"
    

class Queue(models.Model):
    club = models.ForeignKey(BookClub, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.member is not None:
            return f"{self.member.username} added {self.book.name} to the queue"
        else:
            return "Queue object with no member"
        

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s comment on {self.book.name}"