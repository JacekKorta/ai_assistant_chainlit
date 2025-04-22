from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import CustomUser


class AccountsViewsTestCase(TestCase):
    """Test suite for account related views: login, logout, dashboard."""

    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods."""
        # Store the user object directly for force_login
        cls.user = CustomUser.objects.create_user( 
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        cls.login_url = reverse('accounts:login')
        cls.logout_url = reverse('accounts:logout')
        cls.dashboard_url = reverse('accounts:dashboard')
        cls.correct_login_data = { # Still needed for testing actual login process
            'username': 'testuser',
            'password': 'testpassword123'
        }
        cls.incorrect_login_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }

    def setUp(self):
        """Set up client for each test."""
        self.client = Client()

    def test_login_view_get(self):
        """Test GET request to login page returns 200 OK and uses correct template."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_view_post_success(self):
        """Test successful login POST redirects to dashboard and authenticates user."""
        # Here we must use client.post to test the actual login view logic
        response = self.client.post(self.login_url, self.correct_login_data, follow=True) 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/dashboard.html')
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_view_post_failure(self):
        """Test failed login POST re-renders login page and user remains unauthenticated."""

        # Here we must use client.post to test the actual login view logic
        response = self.client.post(self.login_url, self.incorrect_login_data, follow=True) 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertFalse(response.context['user'].is_authenticated)

    def test_logout_view(self):
        """Test logout POST redirects to login page and deauthenticates user."""
        # Log the user in directly using force_login
        self.client.force_login(self.user) 

        # Check POST request for logout - expect redirect
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

        # Verify user is logged out by trying to access dashboard
        response_after_logout = self.client.get(self.dashboard_url)
        self.assertEqual(response_after_logout.status_code, 302)
        self.assertRedirects(response_after_logout, f"{self.login_url}?next={self.dashboard_url}")

    def test_dashboard_view_unauthenticated(self):
        """Test GET request to dashboard by unauthenticated user redirects to login."""
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{self.login_url}?next={self.dashboard_url}")

    def test_dashboard_view_authenticated(self):
        """Test GET request to dashboard by authenticated user returns 200 OK and correct template."""
        # Log the user in directly using force_login
        self.client.force_login(self.user) 
        
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/dashboard.html')
