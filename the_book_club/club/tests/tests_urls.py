from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class UnauthenticatedUserTests(TestCase):
    def setUp(self):
        # Initialize the client
        self.client = Client()

    def test_unauthenticated_user_can_access_public_urls(self):
        # Test that an unauthenticated user can access public URLs
        public_urls = [
            reverse('club:index'),
            reverse('club:book_clubs'),
            reverse('club:books'),
            # Add more public URLs here as needed
        ]

        for url in public_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

        # Optionally, you can test specific view templates here
        # Example:
        response = self.client.get(reverse('club:login'))
        self.assertTemplateUsed(response, 'club/login.html')

        response = self.client.get(reverse('club:register'))
        self.assertTemplateUsed(response, 'club/register.html')

    def test_unauthenticated_user_cannot_access_protected_urls(self):
        # Test that an unauthenticated user is redirected to the login page
        # when trying to access protected URLs
        protected_urls = [
            reverse('club:account'),
            reverse('club:edit_profile'),
            # Add more protected URLs here as needed
        ]

        for url in protected_urls:
            response = self.client.get(url)
            self.assertRedirects(response, reverse('club:login') + '?next=' + url)

class AuthenticatedUserTests(TestCase):
    def setUp(self):
        # Create a user and log them in
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def test_authenticated_user_can_access_protected_urls(self):
        # Test that an authenticated user can access protected URLs
        protected_urls = [
            reverse('club:account'),
            reverse('club:edit_profile'),
            # Add more protected URLs here as needed
        ]

        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

        # Optionally, you can test specific view templates here
        # Example:
        response = self.client.get(reverse('club:account'))
        self.assertTemplateUsed(response, 'club/account.html')
