from django.shortcuts import render, get_object_or_404
from .models import BookClub, ClubPage, Book, BookPage

def index(request):
    return render(request, 'club/index.html')

def book_clubs(request):
    clubs = BookClub.objects.all()
    books = Book.objects.all()
    context = {
        'clubs': clubs,
        'books':books
    }
    return render(request, 'club/book_clubs.html', context)

def books(request):
    books = Book.objects.all()
    context = {
        'books':books
    }
    return render(request, 'club/books.html', context)

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'club/book_detail.html', {'book': book})

def club_detail(request, club_id):
    club = get_object_or_404(BookClub, id=club_id)
    return render(request, 'club/club_detail.html', {'club': club})