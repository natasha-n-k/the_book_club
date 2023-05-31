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
    meeting = models.OneToOneField('Meeting', on_delete=models.SET_NULL, null=True)
    read_books = models.ManyToManyField(Book, related_name='read_clubs')
    book_queue = models.ManyToManyField(Book, through='Queue', related_name='queued_clubs')
    book_queue_members = models.ManyToManyField(User, through='Queue', related_name='queued_books')

    def __str__(self):
        return self.name

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

class Meeting(models.Model):
    date = models.DateField()
    location = models.CharField(max_length=100)
    location_link = models.URLField(null=True, blank=True)

    

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