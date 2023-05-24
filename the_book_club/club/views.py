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
from .models import BookClub, Book,  Rating, UserBook, Meeting, Queue
from .forms import ClubAdminForm, BookSelectionForm, BookQueueForm
from datetime import date
import datetime

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

def club_detail(request, club_id):
    club = get_object_or_404(BookClub, id=club_id)
    return render(request, 'club/club_detail.html', {'club': club})

def books(request):
    books = Book.objects.all()
    context = {
        'books':books
    }
    return render(request, 'club/books.html', context)

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user_book, created = UserBook.objects.get_or_create(user=request.user, book=book)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        if rating is not None:
            rating = int(rating)
            Rating.objects.update_or_create(user=request.user, book=book, defaults={'rating': rating})
            average_rating = book.calculate_average_rating()
            book.average_rating = round(average_rating, 1) if average_rating else None
            book.save()

        status = request.POST.get('status')
        if status in ['to_read', 'read']:
            user_book.status = status
            if status == 'read':
                user_book.date_read = datetime.date.today()
            else:
                user_book.date_read = None
            user_book.save()

            return JsonResponse({
                'success': True,
                'status_text': user_book.get_status_display(),
                'date_read': user_book.date_read.strftime('%Y-%m-%d') if user_book.date_read else None
            })

    return render(request, 'club/book_detail.html', {'book': book, 'user_book': user_book})

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
    current_status = user_book.status

    if current_status != status:
        if status == 'to_read':
            user_book.is_want_to_read = True
            user_book.is_read = False
            user_book.date_read = None
            status_text = 'Хочу прочитать'
        elif status == 'read':
            user_book.is_want_to_read = False
            user_book.is_read = True
            user_book.date_read = date.today()
            status_text = 'Прочитана'
        else:
            user_book.is_want_to_read = False
            user_book.is_read = False
            user_book.date_read = None
            status_text = 'Не выбрано'

        user_book.status = status
        user_book.save()

        return JsonResponse({'success': True, 'status_text': status_text})
    else:
        return JsonResponse({'success': True, 'status_text': user_book.get_status_display()})

def rate_book(request, book_id):
    if request.method == 'POST':
        rating = float(request.POST.get('rating'))
        book = Book.objects.get(id=book_id)
        user = request.user
        Rating.objects.create(book=book, user=user, rating=rating)
        book.average_rating = book.calculate_average_rating()
        book.save()
    return redirect('club:book_detail', book_id=book_id)

from django.shortcuts import get_object_or_404
    
@login_required
def mark_book_read(request, club_id):
    club = get_object_or_404(BookClub, id=club_id)
    
    if request.method == 'POST' and request.user == club.admin:
        club.selected_book = None
        club.save()
        messages.success(request, 'Книга успешно отмечена как прочитанная!')
    else:
        messages.error(request, 'У вас нет прав для отметки книги как прочитанной.')
    
    return redirect('club:club_detail', club_id=club_id)

def club_admin(request, club_id):
    club = BookClub.objects.get(id=club_id)

    if request.method == 'POST':
        selection_form = BookSelectionForm(request.POST)
        queue_form = BookQueueForm(request.POST, club_id=club_id)

        if selection_form.is_valid():
            book = selection_form.cleaned_data['book']
            club.selected_book = book
            club.save()
            return redirect('club:club_detail', club_id=club_id)

        if queue_form.is_valid():
            book = queue_form.cleaned_data['book']
            club.book_queue.add(book)
            return redirect('club:club_detail', club_id=club_id)
    else:
        selection_form = BookSelectionForm()
        queue_form = BookQueueForm(club_id=club_id)

    return render(request, 'club/admin.html', {'club': club, 'selection_form': selection_form, 'queue_form': queue_form})

def add_to_queue(request, club_id):
    if request.method == 'POST':
        book_id = request.POST.get('book')
        club = BookClub.objects.get(id=club_id)
        book = Book.objects.get(id=book_id)
        club.book_queue.add(book)
        return redirect('club:club_admin', club_id=club_id)
    
def select_book(request, club_id):
    if request.method == 'POST':
        book_id = request.POST.get('book')
        book = Book.objects.get(id=book_id)
        club = BookClub.objects.get(id=club_id)
        club.selected_book = book
        club.save()
        return redirect('club:club_admin', club_id=club_id)
