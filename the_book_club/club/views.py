from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.contrib import messages
from django.http import JsonResponse
from .models import BookClub, Book,  Rating, UserBook
from datetime import date

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

@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        Rating.objects.update_or_create(user=request.user, book=book, defaults={'rating': rating})
        ratings = Rating.objects.filter(book=book)
        average_rating = ratings.aggregate(models.Avg('rating')).get('rating__avg')
        book.average_rating = round(average_rating, 1) if average_rating else None
        book.save()

        return JsonResponse({'success': True})

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
    read_books = UserBook.objects.filter(user=request.user, is_read=True)
    want_to_read_books = UserBook.objects.filter(user=request.user, is_want_to_read=True)
    return render(request, 'club/account.html', {'clubs': clubs, 'read_books': read_books, 'want_to_read_books': want_to_read_books})

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
        return redireFalsect('club:account')
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
    
@login_required
def update_book_status(request, book_id, status):
    book = get_object_or_404(Book, id=book_id)
    user_book, created = UserBook.objects.get_or_create(user=request.user, book=book)
    if status == 'to_read':
        user_book.is_want_to_read = True
        user_book.is_read = False
        user_book.date_read = None
    elif status == 'read':
        user_book.is_want_to_read = False
        user_book.is_read = True
        user_book.date_read = date.today()
    user_book.save()
    return JsonResponse({'success': True})

def rate_book(request, book_id, rating):
    book = Book.objects.get(id=book_id)
    user = request.user
    if Rating.objects.filter(book=book, user=user).exists():
        book_rating = Rating.objects.get(book=book, user=user)
        book_rating.rating = rating
    else:
        book_rating = Rating.objects.create(book=book, user=user, rating=rating)
    book_rating.save()
    average_rating = Rating.objects.get_average_rating(book=book)
    return JsonResponse({'success': True, 'average_rating': average_rating})