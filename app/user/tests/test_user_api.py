"""
Tests for the user API
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

# The create user api url
CREATE_USER_URL = reverse('user:create')

# Token endpoint url
TOKEN_URL=reverse('user:token')


# Create a test user object for testing purposes
def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public user API"""

    def setUp(self):
        """Create the APIClient"""
        self.client = APIClient()

    def test_create_user_success(self):
        """Test user creation is successful"""
        # Create our test user values
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        # Create the user and get results
        res = self.client.post(CREATE_USER_URL, payload)

        # Test that return code was 201 as expected
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Get the user object that was created
        user = get_user_model().objects.get(email=payload['email'])

        # Check the password was entered correctly
        self.assertTrue(user.check_password(payload['password']))

        # make sure password hash not returned
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if email already exists"""
        # Create our test user values
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }

        # User our function above to create a user from payload
        create_user(**payload)

        # Now try using the API to create the same user
        res = self.client.post(CREATE_USER_URL, payload)

        # Check the return code was bad request
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is thrown for password under 5 characters"""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test Name',
        }

        # Try to create the user with short password
        res = self.client.post(CREATE_USER_URL, payload)

        # Check the return code was bad request
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # Get the user object
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        # Ensure the user doesn't exist
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test generate token for valid credentials"""
        # Create a user object for an existing user
        user_details = {
            'name':'Test Name',
            'email': 'test@example.com',
            'password': 'test-user-password123',
        }
        create_user(**user_details)

        # Create a payload to send to the token API
        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid"""
        # Create test user
        create_user(email='test@example.com', password='goodpass')

        # Create payload for token api with wrong password
        payload = {'email': 'test@example.com','password': 'badpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error"""
        # Create payload for token api with blank password
        payload = {'email': 'test@example.com','password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)