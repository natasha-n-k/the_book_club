from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from .models import BookClub, Book
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages

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

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login


@csrf_protect
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            user_login(request, user)
            messages.success(request, f'Добро пожаловать, {username}!')
            if request.user.is_authenticated:  # проверяем, авторизован ли пользователь
                return redirect('club:account')  # если авторизован, перенаправляем на страницу личного кабинета
            else:
                return redirect('club:login')  # если не авторизован, перенаправляем на страницу входа
        else:
            error_message = 'Неверные имя пользователя или пароль'
            return render(request, 'club/login.html', {'error_message': error_message})
    else:
        return render(request, 'club/login.html')
    
def logout(request):
    auth_logout(request)
    return redirect('club:login')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('club:login')
    else:
        form = UserCreationForm()
    return render(request, 'club/register.html', {'form': form})

@login_required
def account(request):
    clubs = BookClub.objects.filter(members=request.user)
    want_to_read_books = Book.objects.filter(users_who_want_to_read=request.user)
    read_books = Book.objects.filter(users_who_read=request.user)
    return render(request, 'club/account.html', {'clubs': clubs, 'want_to_read_books': want_to_read_books, 'read_books': read_books})