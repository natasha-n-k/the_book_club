from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from club.models import BookClub, Book
from django.core.files.uploadedfile import SimpleUploadedFile

class ViewsTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Create some test book clubs with image files
        image_file = SimpleUploadedFile("8.jpg", b"file_content", content_type="image/jpeg")
        self.club1 = BookClub.objects.create(name='Club 1', description='Test description 1', image=image_file)
        self.club2 = BookClub.objects.create(name='Club 2', description='Test description 2', image=image_file)
        
        # Create some test books with image files
        book_image_file = SimpleUploadedFile("12.jpg", b"file_content", content_type="image/jpeg")
        self.book1 = Book.objects.create(name='Book 1', description='Test book description 1', image=book_image_file)
        self.book2 = Book.objects.create(name='Book 2', description='Test book description 2', image=book_image_file)

    def test_index_view(self):
        # Test the index view
        client = Client()
        response = client.get(reverse('club:index'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club/index.html')
        self.assertContains(response, 'Club 1')  # Assuming 'Club 1' is displayed in the index template
        self.assertContains(response, 'Club 2')  # Assuming 'Club 2' is displayed in the index template

    def test_book_clubs_view(self):
        # Test the book clubs view
        client = Client()
        response = client.get(reverse('club:book_clubs'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club/book_clubs.html')
        self.assertContains(response, 'Club 1')  # Assuming 'Club 1' is displayed in the book clubs template
        self.assertContains(response, 'Club 2')  # Assuming 'Club 2' is displayed in the book clubs template

    def test_club_detail_view(self):
        # Test the club detail view
        client = Client()
        response = client.get(reverse('club:club_detail', kwargs={'club_id': self.club1.id}))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club/club_detail.html')
        self.assertContains(response, 'Club 1')  # Assuming 'Club 1' is displayed in the club detail template

    def test_books_view(self):
        # Test the books view
        client = Client()
        response = client.get(reverse('club:books'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club/books.html')
        self.assertContains(response, 'Book 1')  # Assuming 'Book 1' is displayed in the books template
        self.assertContains(response, 'Book 2')  # Assuming 'Book 2' is displayed in the books template

    def test_book_detail_view(self):
        # Test the book detail view
        client = Client()
        response = client.get(reverse('club:book_detail', kwargs={'book_id': self.book1.id}))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club/book_detail.html')
        self.assertContains(response, 'Book 1')  # Assuming 'Book 1' is displayed in the book detail template

