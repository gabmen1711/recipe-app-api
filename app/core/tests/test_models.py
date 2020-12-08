from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email="gjmm3012@gmail.com", password="admin123"):
    """Create a sample user"""
    return get_user_model().objects.create_user(
        email=email,
        password=password
    )


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """
        Test creating a new user with email is successful
        """
        email = "gjmm1711@gmail.com"
        password = "admin123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = "gjmm17177@GMAIL.COM"
        user = get_user_model().objects.create_user(email, "admin123")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "admin123")

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            "gjmm1711@gmail.com",
            "admin123"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name="Vegan"
        )
        self.assertEqual(str(tag), tag.name)
