from django.contrib import admin
from .models import BookClub, ClubPage, Book, BookPage


# Register your models here.
admin.site.register(BookClub)
admin.site.register(ClubPage)
admin.site.register(Book)
admin.site.register(BookPage)

