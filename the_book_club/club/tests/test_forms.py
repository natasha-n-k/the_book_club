from django.test import TestCase
from club.forms import ClubAdminForm, UserCreationForm, BookSelectionForm, BookQueueForm, MeetingForm, BookClubForm
from club.models import BookClub, Book

class FormsTest(TestCase):

    def test_user_creation_form_valid(self):
        # Test valid data
        form_data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_creation_form_invalid(self):
        # Test invalid data (passwords do not match)
        form_data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'differentpassword',
        }
        form = UserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_book_selection_form_valid(self):
        # Test valid data
        form_data = {
            'book': 1,  # Replace with a valid book ID from your database
        }
        form = BookSelectionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_book_selection_form_invalid(self):
        # Test invalid data (missing required fields)
        form_data = {
            # 'book' field is missing
        }
        form = BookSelectionForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_book_queue_form_valid(self):
        # Test valid data
        club = BookClub.objects.create(name='Test Club', description='Test Club Description')
        book = Book.objects.create(name='Test Book', description='Test Book Description')
        club.book_queue.add(book)
        form_data = {
            'book': book.id,
        }
        form = BookQueueForm(data=form_data, club_id=club.id)
        self.assertTrue(form.is_valid())

    def test_book_queue_form_invalid(self):
        # Test invalid data (book already in the club's queue)
        club = BookClub.objects.create(name='Test Club', description='Test Club Description')
        book = Book.objects.create(name='Test Book', description='Test Book Description')
        club.book_queue.add(book)
        form_data = {
            'book': book.id,
        }
        form = BookQueueForm(data=form_data, club_id=club.id)
        self.assertFalse(form.is_valid())

    def test_meeting_form_valid(self):
        # Test valid data
        form_data = {
            'meeting_date': '2023-07-20',
            'location': 'Test Location',
            'location_link': 'https://example.com',
        }
        form = MeetingForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_meeting_form_invalid(self):
        # Test invalid data (missing required fields)
        form_data = {
            # 'meeting_date', 'location', and 'location_link' fields are missing
        }
        form = MeetingForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_book_club_form_valid(self):
        # Test valid data
        form_data = {
            'name': 'Test Club',
            'description': 'Test Club Description',
            # Provide required data for other fields as well
        }
        form = BookClubForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_book_club_form_invalid(self):
        # Test invalid data (missing required fields)
        form_data = {
            # 'name', 'description', and other required fields are missing
        }
        form = BookClubForm(data=form_data)
        self.assertFalse(form.is_valid())