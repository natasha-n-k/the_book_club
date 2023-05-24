from django.contrib import admin
from .models import BookClub, Book, UserBook, Rating, Meeting, Queue, Profile


# Register your models here.
admin.site.register(BookClub)
admin.site.register(Book)
admin.site.register(UserBook)
admin.site.register(Rating)
admin.site.register(Meeting)
admin.site.register(Queue)
admin.site.register(Profile)

