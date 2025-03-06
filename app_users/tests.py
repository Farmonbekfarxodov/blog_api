from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from unittest.mock import patch

User = get_user_model()


class RegisterViewTest(APITestCase):
    def setUp(self):
        self.register_url = "/users/register/"
        self.valid_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "Test@1234"
        }

    @patch("app_users.views.send_verification_email")  # Email jo‘natish funksiyasini mock qilamiz
    def test_successful_registration(self, mock_send_email):
        response = self.client.post(self.register_url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Emailga tasdiqlash kodi yuborildi!")
        user = User.objects.get(email=self.valid_data["email"])
        self.assertFalse(user.email_verified)  # Email tasdiqlanmagan bo‘lishi kerak
        self.assertIsNotNone(user.verification_code)  # Tasdiqlash kodi generatsiya qilingan bo‘lishi kerak
        mock_send_email.assert_called_once_with(user.email, user.verification_code)

    def test_registration_with_invalid_data(self):
        invalid_data = {
            "username": "",
            "email": "invalid-email",
            "password": "short"
        }
        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertIn("password", response.data)
        self.assertIn("username", response.data)

    def test_duplicate_email_registration(self):
        User.objects.create_user(**self.valid_data)
        response = self.client.post(self.register_url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
