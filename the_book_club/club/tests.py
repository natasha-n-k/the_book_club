from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import BookClub, Book, Rating, UserBook, Meeting, Queue

class ClubTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.club = BookClub.objects.create(name='Test Club', admin=self.user)

    def test_index_page(self):
        response = self.client.get(reverse('club:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club/index.html')


    def test_book_clubs_page(self):
        response = self.client.get(reverse('club:book_clubs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club/book_clubs.html')

    def test_club_detail_page(self):
        response = self.client.get(reverse('club:club_detail', args=[self.club.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club/club_detail.html')

    def test_books_page(self):
        response = self.client.get(reverse('club:books'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club/books.html')

    def test_book_detail_page(self):
        book = Book.objects.create(name='Test Book')
        response = self.client.get(reverse('club:book_detail', args=[book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club/book_detail.html')

    def test_user_login(self):
        response = self.client.post(reverse('club:login'), {'login': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertRedirects(response, reverse('club:account'))

    def test_user_logout(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('club:logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout
        self.assertRedirects(response, reverse('club:login'))

    def test_user_register(self):
        response = self.client.post(reverse('club:register'), {'username': 'newuser', 'password1': 'testpassword', 'password2': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertRedirects(response, reverse('club:account'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_join_club(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('club:join_club', args=[self.club.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after joining club
        self.assertRedirects(response, reverse('club:club_detail', args=[self.club.id]))
        self.assertTrue(self.user.bookclub_set.filter(id=self.club.id).exists())

    def test_update_book_status(self):
        book = Book.objects.create(name='Test Book')
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('club:update_book_status', args=[book.id, 'to_read']))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['success'], True)
        self.assertEqual(data['status_text'], 'Хочу прочитать')

    def test_rate_book(self):
        book = Book.objects.create(name='Test Book')
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('club:rate_book', args=[book.id]), {'rating': '4.5'})
        self.assertEqual(response.status_code, 302)  # Redirect after rating book
        self.assertRedirects(response, reverse('club:book_detail', args=[book.id]))
        self.assertEqual(Rating.objects.filter(book=book, user=self.user, rating=4.5).count(), 1)

    def test_create_book_club(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('club:create_book_club'), {'name': 'New Club', 'admin': self.user.id})
        self.assertEqual(response.status_code, 302)  # Redirect after creating book club
        self.assertRedirects(response, reverse('club:club_detail', args=[BookClub.objects.latest('id').id]))
        self.assertTrue(BookClub.objects.filter(name='New Club').exists())
