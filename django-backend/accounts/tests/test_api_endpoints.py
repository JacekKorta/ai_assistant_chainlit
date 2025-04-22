from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class VerifyCredentialsAPITestCase(APITestCase):
    """Test suite for the credentials verification API endpoint."""

    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods."""
        cls.test_user = CustomUser.objects.create_user(
            username='apiuser',
            email='api@example.com',
            password='apipassword123'
        )
        # Assume the URL name for the endpoint will be 'verify_credentials'
        # within an app namespace 'accounts_api' (we'll define this later)
        cls.verify_url = reverse('accounts_api:verify_credentials') 
        cls.correct_credentials = {
            'username': 'apiuser',
            'password': 'apipassword123'
        }
        cls.incorrect_password_credentials = {
            'username': 'apiuser',
            'password': 'wrongpassword'
        }
        cls.non_existent_user_credentials = {
            'username': 'nouser',
            'password': 'anypassword'
        }

    def test_verify_credentials_success(self):
        """Test successful credential verification returns 200 OK."""
        response = self.client.post(self.verify_url, self.correct_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'ok'})

    def test_verify_credentials_incorrect_password(self):
        """Test incorrect password returns 401 Unauthorized."""
        response = self.client.post(self.verify_url, self.incorrect_password_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_verify_credentials_non_existent_user(self):
        """Test non-existent user returns 401 Unauthorized."""
        response = self.client.post(self.verify_url, self.non_existent_user_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_verify_credentials_missing_username(self):
        """Test request missing username returns 400 Bad Request."""
        data = {'password': 'apipassword123'}
        response = self.client.post(self.verify_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_credentials_missing_password(self):
        """Test request missing password returns 400 Bad Request."""
        data = {'username': 'apiuser'}
        response = self.client.post(self.verify_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_credentials_get_not_allowed(self):
        """Test GET request is not allowed (405)."""
        response = self.client.get(self.verify_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_verify_credentials_put_not_allowed(self):
        """Test PUT request is not allowed (405)."""
        response = self.client.put(self.verify_url, self.correct_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_verify_credentials_delete_not_allowed(self):
        """Test DELETE request is not allowed (405)."""
        response = self.client.delete(self.verify_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
