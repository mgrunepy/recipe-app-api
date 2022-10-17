"""
Tests for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test Models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        email = "test@example.com"
        password = "testpass1234"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test emails are normalized"""
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["test2@EXAMPLE.COM", "test2@example.com"],
            ["Test3@EXAMPLE.COM", "Test3@example.com"],
            ["TEST4@EXAMPLE.COM", "TEST4@example.com"],
            ["test5@Example.com", "test5@example.com"],
            ["test6@Example.Com", "test6@example.com"],
            ["TeSt7@ExaMplE.cOm", "TeSt7@example.com"],
            ["test8@example.com", "test8@example.com"],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "sample1234")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test creating a user without an email will raise a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test123")

    def test_create_superuser(self):
        """Test creating super user"""
        user = get_user_model().objects.create_superuser(
            "test@emample.com",
            "test1234"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
