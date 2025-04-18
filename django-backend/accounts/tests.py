from django.test import TestCase, Client
from django.urls import reverse
from .models import CustomUser


class AccountsTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.client = Client()

    def test_login_view(self):
        # Test widoku logowania
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        
        # Test logowania z poprawnymi danymi
        login_data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        response = self.client.post(reverse('accounts:login'), login_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.client.logout()
        
        # Test logowania z nieprawidłowymi danymi
        login_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('accounts:login'), login_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_logout_view(self):

        self.client.force_login(self.user)
        
        # Sprawdź czy wylogowanie działa
        response = self.client.post(reverse('accounts:logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
        
    def test_dashboard_view(self):
        # Test dostępu do dashboard gdy niezalogowany
        response = self.client.get(reverse('accounts:dashboard'))
        self.assertNotEqual(response.status_code, 200)
        
        # Zaloguj użytkownika
        self.client.force_login(self.user)
        
        # Test dostępu do dashboard gdy zalogowany
        response = self.client.get(reverse('accounts:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/dashboard.html')
