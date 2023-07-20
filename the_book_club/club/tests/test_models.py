from django.test import TestCase
from club.models import Profile, Book, BookClub, UserBook, Rating, Meeting, Queue
from django.contrib.auth.models import User
from decimal import Decimal

class ProfileModelTest(TestCase):
    def test_profile_str(self):
        # Test the __str__ method of the Profile model
        user = User.objects.create_user(username='testuser', password='testpassword')
        profile = Profile.objects.create(user=user)
        self.assertEqual(str(profile), 'testuser')

class BookModelTest(TestCase):
    def test_book_str(self):
        # Test the __str__ method of the Book model
        book = Book.objects.create(name='Test Book', description='Test description')
        self.assertEqual(str(book), 'Test Book')

    def test_calculate_average_rating(self):
        # Test the calculate_average_rating method of the Book model
        book = Book.objects.create(name='Test Book', description='Test description')
        user = User.objects.create_user(username='testuser', password='testpassword')
        Rating.objects.create(book=book, user=user, rating=4.5)
        Rating.objects.create(book=book, user=user, rating=3.0)
        average_rating = book.calculate_average_rating()
        self.assertEqual(average_rating, Decimal('3.75'))

class BookClubModelTest(TestCase):
    def test_book_club_str(self):
        # Test the __str__ method of the BookClub model
        book_club = BookClub.objects.create(name='Test Club', description='Test description')
        self.assertEqual(str(book_club), 'Test Club')

class UserBookModelTest(TestCase):
    def test_user_book_str(self):
        # Test the __str__ method of the UserBook model
        user = User.objects.create_user(username='testuser', password='testpassword')
        book = Book.objects.create(name='Test Book', description='Test description')
        user_book = UserBook.objects.create(user=user, book=book)
        self.assertEqual(str(user_book), "testuser's Test Book")

class RatingModelTest(TestCase):
    def test_rating_str(self):
        # Test the __str__ method of the Rating model
        user = User.objects.create_user(username='testuser', password='testpassword')
        book = Book.objects.create(name='Test Book', description='Test description')
        rating = Rating.objects.create(user=user, book=book, rating=4.5)
        self.assertEqual(str(rating), "testuser's rating for Test Book")

class MeetingModelTest(TestCase):
    def test_meeting_str(self):
        # Test the __str__ method of the Meeting model
        book_club = BookClub.objects.create(name='Test Club', description='Test description')
        meeting = Meeting.objects.create(date='2023-07-20', location='Test Location')
        meeting.club.add(book_club)
        self.assertEqual(str(meeting), "Meeting for Test Club")

class QueueModelTest(TestCase):
    def test_queue_str(self):
        # Test the __str__ method of the Queue model
        book_club = BookClub.objects.create(name='Test Club', description='Test description')
        book = Book.objects.create(name='Test Book', description='Test description')
        user = User.objects.create_user(username='testuser', password='testpassword')
        queue = Queue.objects.create(club=book_club, member=user, book=book)
        self.assertEqual(str(queue), "testuser added Test Book to the queue")
