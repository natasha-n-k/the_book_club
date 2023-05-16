from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from .models import BookClub, Book
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
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


@csrf_protect
def user_login(request):
    if request.method == 'POST':
        login = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, username=login, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('club:account')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('club:login')
    else:
        return render(request, 'club/login.html')

@login_required
def account(request):
    clubs = BookClub.objects.filter(members=request.user)
    return render(request, 'club/account.html', {'clubs': clubs})

def user_logout(request):
    logout(request)
    return redirect('club:login')

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Ваша учетная запись была успешно создана!')
            return redirect('club:account')
    else:
        form = UserCreationForm()
    return render(request, 'club/register.html', {'form': form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.date_of_birth = request.POST.get('date_of_birth')
        user.save()
        return redirect('club:account')
    else:
        return render(request, 'club/edit_profile.html')

@login_required
def join_club(request, club_id):
    if request.method == 'POST':
        club = get_object_or_404(BookClub, id=club_id)
        club.members.add(request.user)
        messages.success(request, f'You have joined the "{club.name}" book club!')
        return redirect('club:book_clubs')
    else:
        clubs = BookClub.objects.all()
        context = {
            'clubs': clubs
        }
        return render(request, 'club/book_clubs.html', context)