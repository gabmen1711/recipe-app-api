from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test de users API public"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            "email": "gjmm3012@gmail.com",
            "password": "testpass",
            "name": "Luke Skywalker"
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_exist(self):
        """Test creating an user that already exist"""
        payload = {
            "email": "gjmm3012@gmail.com",
            "password": "testpass",
            "name": "Han Solo"
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Password must be more than 5 characters"""
        payload = {
            "email": "gjmm3012@gmail.com",
            "password": "pw",
            "name": "Anakin Skywalker"
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertTrue(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().objects.filter(
            email=payload["email"]
        ).exists()
        self.assertFalse(user_exist)

    def test_create_token_for_user(self):
        """Test that a token is created for user"""
        payload = dict(
            email="gjmm3012@gmail.com",
            password="admin123"
        )
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_crete_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials given"""
        create_user(
            email="gjmm3012@gmail.com",
            password="admin123"
        )
        payload = dict(
            email="gjmm3012@gmail.com",
            password="admin111"
        )
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test for not creating token if user does not exist"""
        payload = dict(
            email="gjmm3012@gmail.com",
            password="admin123"
        )
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test email and password is not required"""
        payload = dict(
            email="gjmm3012@gmail.com",
            password=""
        )
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
