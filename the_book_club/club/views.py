from django.shortcuts import render
from .models import BookClub, ClubPage, Book, BookPage

def index(request):
    return render(request, 'club/index.html')

def book_clubs(request):
    clubs = BookClub.objects.all()
    context = {
        'clubs': clubs
    }
    return render(request, 'club/book_clubs.html', context)