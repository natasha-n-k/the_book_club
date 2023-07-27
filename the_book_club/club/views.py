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
from django.db.models import Q
from .models import BookClub, Book,  Rating, UserBook, Meeting, Queue, Comment
from .forms import ClubAdminForm, BookSelectionForm, BookQueueForm, MeetingForm, BookClubForm
from datetime import date
from django.urls import reverse
import datetime

def index(request):
    clubs = BookClub.objects.all()[:4] 
    return render(request, 'club/index.html', {'clubs': clubs})

def book_clubs(request):
    clubs = BookClub.objects.all()
    genres = BookClub.objects.values_list('genre', flat=True).distinct()
    themes = BookClub.objects.values_list('theme', flat=True).distinct()
    genre = request.GET.get('genre')
    theme = request.GET.get('theme')
    if genre:
        clubs = clubs.filter(genre=genre)
    if theme:
        clubs = clubs.filter(theme=theme)
    context = {
        'clubs': clubs,
        'genres': genres,
        'themes': themes,
    }
    return render(request, 'club/book_clubs.html', context)

def club_detail(request, club_id):
    club = get_object_or_404(BookClub, id=club_id)
    book_queue = Queue.objects.filter(club=club)

    return render(request, 'club/club_detail.html', {'club': club, 'book_queue': book_queue})

def books(request):
    books = Book.objects.all()
    genres = Book.objects.values_list('genre', flat=True).distinct()
    themes = Book.objects.values_list('theme', flat=True).distinct()
    genre = request.GET.get('genre')
    theme = request.GET.get('theme')
    search_query = request.GET.get('search')

    if genre:
        books = books.filter(genre=genre)
    if theme:
        books = books.filter(theme=theme)
    if search_query:
        search_words = search_query.strip().split()
        query = Q()
        for word in search_words:
            query |= Q(name__icontains=word) | Q(author__icontains=word)
        books = books.filter(query)

    context = {
        'books': books,
        'genres': genres,
        'themes': themes
    }
    return render(request, 'club/books.html', context)

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user = request.user

    if not user.is_authenticated:
        user = None

    user_book, created = UserBook.objects.get_or_create(user=user, book=book)
    comments = Comment.objects.filter(book=book).order_by('-created_at')

    if request.method == 'POST':
        rating = request.POST.get('rating')
        if rating is not None:
            rating = int(rating)
            Rating.objects.update_or_create(user=user, book=book, defaults={'rating': rating})
            average_rating = book.calculate_average_rating()
            book.average_rating = round(average_rating, 1) if average_rating else None
            book.save()

        status = request.POST.get('status')
        if status in ['to_read', 'read'] and user.is_authenticated:
            user_book.status = status
            if status == 'read':
                user_book.date_read = date.today()
            else:
                user_book.date_read = None
            user_book.save()  # Save the updated UserBook here

            # Optionally, you can redirect back to the same page after the update
            return redirect('club:book_detail', book_id=book_id)

        comment_text = request.POST.get('comment_text')
        if comment_text:
            if user.is_authenticated:
                comment = Comment.objects.create(user=user, book=book, text=comment_text)
                comments = Comment.objects.filter(book=book).order_by('-created_at')

    return render(request, 'club/book_detail.html', {'book': book, 'user_book': user_book, 'comments': comments})

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
    # Filter UserBook objects based on is_want_to_read and is_read fields
    want_to_read_books = UserBook.objects.filter(user=request.user, is_want_to_read=True, is_read=False)
    read_books = UserBook.objects.filter(user=request.user, is_want_to_read=False, is_read=True)
    return render(request, 'club/account.html', {'clubs': clubs, 'read_books': read_books, 'want_to_read_books': want_to_read_books})

def user_logout(request):
    logout(request)
    return redirect('club:login')

def user_register(request):
    form_submitted = False
    if request.method == 'POST':
        form_submitted = True
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Ваша учетная запись была успешно создана!')
            return redirect('club:account')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = UserCreationForm()
    return render(request, 'club/register.html', {'form': form, 'form_submitted': form_submitted})

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
        return redirect('club:club_detail', club_id=club.id)
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
        previous_rating = Rating.objects.filter(user=user, book=book).first()

        if previous_rating:
            previous_rating.delete()

        Rating.objects.create(book=book, user=user, rating=rating)
        book.average_rating = book.calculate_average_rating()
        book.save()

    return redirect('club:book_detail', book_id=book_id)


@login_required
def club_admin(request, club_id):
    club = get_object_or_404(BookClub, id=club_id)
    selection_form = BookSelectionForm()
    queue_form = BookQueueForm(club_id=club_id)
    meeting_form = MeetingForm()
    book_queue = Queue.objects.filter(club=club)
    meetings = Meeting.objects.all()

    if request.method == 'POST':
        selection_form = BookSelectionForm(request.POST)
        queue_form = BookQueueForm(request.POST, club_id=club_id)
        meeting_form = MeetingForm(request.POST)
        if 'selected_book' in request.POST:
            if selection_form.is_valid():
                book = selection_form.cleaned_data['book']
                club.selected_book = book
                club.save()
                return redirect('club:club_admin', club_id=club_id)

        if 'add_to_queue' in request.POST:
            queue_form = BookQueueForm(request.POST, club_id=club_id)
            if queue_form.is_valid():
                book = queue_form.cleaned_data['book']
                club.book_queue.add(book)
                return redirect('club:club_detail', club_id=club_id)

        if 'meeting_date' in request.POST:
            meeting_form = MeetingForm(request.POST)
            if meeting_form.is_valid():
                date = meeting_form.cleaned_data['meeting_date']
                location = meeting_form.cleaned_data['meeting_location']
                location_link = meeting_form.cleaned_data['meeting_location_link']
                Meeting.objects.create(club=club, date=date, location=location, location_link=location_link)
                return redirect('club:admin', club_id=club.id)
            
        else:
            selection_form = BookSelectionForm()
            queue_form = BookQueueForm(club_id=club_id)
            meeting_form = MeetingForm()

    context = {
        'club': club,
        'book_queue': book_queue,
        'meetings': meetings,
        'selection_form': selection_form,
        'queue_form': queue_form,
        'meeting_form': meeting_form,
    }

    return render(request, 'club/admin.html', context)

def add_to_queue(request, club_id):
    if request.method == 'POST':
        club = get_object_or_404(BookClub, id=club_id)
        book_id = request.POST.get('book')
        book = Book.objects.get(id=book_id)
        club.book_queue.add(book)
        return redirect('club:club_admin', club_id=club_id)
    
def append_to_queue(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        member = request.user 
        club_id = request.POST.get('club')
        club = get_object_or_404(BookClub, id=club_id)
        queue = Queue.objects.create(book=book, member=member, club=club)
        return redirect('club:book_detail', book_id=book_id)
    
def select_book(request, club_id):
    if request.method == 'POST':
        book_id = request.POST.get('book')
        book = Book.objects.get(id=book_id)
        club = BookClub.objects.get(id=club_id)
        club.selected_book = book
        club.save()
        return redirect('club:club_admin', club_id=club_id)
    
def mark_book_read(request, club_id):
    club = BookClub.objects.get(id=club_id)
    selected_book = club.selected_book
    club.read_books.add(selected_book)
    selected_book.status = 'read'
    selected_book.save()
    return redirect('club:club_admin', club_id=club_id)

@require_POST
@login_required
def remove_from_queue(request, club_id):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        queue = Queue.objects.filter(club_id=club_id, book_id=book_id)
        queue.delete()
    return redirect('club:club_admin', club_id=club_id)


def schedule_meeting(request, club_id):
    if request.method == 'POST':
        meeting_date = request.POST.get('meeting_date')
        meeting_location = request.POST.get('meeting_location')
        meeting_location_link = request.POST.get('meeting_location_link')
        club = get_object_or_404(BookClub, id=club_id)
        meeting = Meeting(date=meeting_date, location=meeting_location, location_link=meeting_location_link)
        meeting.save()
        meeting.club.add(club)
        return redirect(reverse('club:club_admin', kwargs={'club_id': club_id}))

    return render(request, 'club/admin.html')

@require_POST
@login_required
def delete_meeting(request, club_id, meeting_id):
    club = get_object_or_404(BookClub, id=club_id)
    meeting = get_object_or_404(Meeting, id=meeting_id)
    meeting.delete()
    return redirect('club:club_admin', club_id=club_id)

@login_required 
def create_book_club(request):
    if request.method == 'POST':
        form = BookClubForm(request.POST, request.FILES)
        if form.is_valid():
            club = form.save(commit=False)
            club.admin = request.user  
            club.save()
            return redirect('club:club_detail', club_id=club.id) 
    else:
        form = BookClubForm()
    
    return render(request, 'club/create_club.html', {'form': form})


def comments(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user = request.user
    user_book, created = UserBook.objects.get_or_create(user=user, book=book)
    comments = Comment.objects.filter(book=book).order_by('-created_at')

    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        if comment_text:
            if request.user.is_authenticated:
                comment = Comment.objects.create(user=request.user, book=book, text=comment_text)
                comments = Comment.objects.filter(book=book).order_by('-created_at')

        rating = request.POST.get('rating')
        if rating is not None:
            rating = int(rating)
            Rating.objects.update_or_create(user=request.user, book=book, defaults={'rating': rating})
            average_rating = book.calculate_average_rating()
            book.average_rating = round(average_rating, 1) if average_rating else None
            book.save()

            return JsonResponse({'average_rating': book.average_rating})

    return render(request, 'club/comments.html', {'book': book, 'user_book': user_book, 'comments': comments})