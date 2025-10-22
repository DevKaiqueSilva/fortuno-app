import json
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fortuno.settings')
django.setup()

from unittest.mock import patch
from django.test import override_settings
from django.core.management import execute_from_command_line
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from app.models.user import User
from freezegun import freeze_time

class TestUserView(APITestCase):
    def test_login(self):
        url = reverse('api:user-login')
        response = self.client.post(
            url,
            data={
                'email': 'test@gmail.com',
                'password': 'Pass123@'
            },
        )
        self.assertEqual(
            status.HTTP_401_UNAUTHORIZED,
            response.status_code,
        )
        User.objects.create_user(
            username="test@gmail.com",
            email="test@gmail.com",
            password="Pass123@",
        )
        
        response = self.client.post(
            url,
            data={
                'email': 'test@gmail.com',
                'password': 'Pass123@'
            },
        )
        self.assertEqual(
            status.HTTP_200_OK,
            response.status_code,
        )

    def test_register(self):
        """
            Scenarios:
            1 - With wrong data
            2 - With correct data
        """

        # 1 - With wrong data
        url = reverse('api:user-register')
        response = self.client.post(
            url,
            data={
                'email': 'XXXX',
                'password': 'XXXX',
                'firstName': 'XXXX',
                'lastName': 'XXXX',
                'phone': 'XXXX',
            },
        )
        self.assertEqual(
            status.HTTP_400_BAD_REQUEST,
            response.status_code,
        )
        self.assertEqual(
            {
                "email":["Enter a valid email address."],
                "password":["Ensure this field has at least 8 characters."]
            },
            response.json()
        )

        # 2 - With correct data
        response = self.client.post(
            url,
            data={
                'email': 'test@gmail.com',
                'password': 'Psswd123@',
                'first_name': 'Testildo',
                'last_name': 'Tester',
                'phone': '11981239322',
            },
        )
        self.assertEqual(
            status.HTTP_200_OK,
            response.status_code,
        )
        User.objects.get(
            username='test@gmail.com',
            email='test@gmail.com',
            first_name='Testildo',
            last_name='Tester',
            phone='11981239322',
        )

    @freeze_time("2025-01-01 12:00:00")
    def test_get_logged_user_info(self):
        url = reverse('api:user-me')
        response = self.client.get(url)
        self.assertEqual(
            status.HTTP_401_UNAUTHORIZED,
            response.status_code,
        )

        user = User.objects.create_user(
            username="test@gmail.com",
            email="test@gmail.com",
            password="Pass123@",
            first_name="Testildo",
            last_name="Tester",
            phone="11981239322",
        )

        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        self.assertEqual(
            status.HTTP_200_OK,
            response.status_code,
        )
        self.assertEqual(
            {
                "email": user.email,
                "firstName": user.first_name,
                "lastName": user.last_name,
                "phone": user.phone,
                "created": "2025-01-01T12:00:00Z",
                "balance": {
                    "totalDebit": 0,
                    "totalCredit": 0,
                }
            },
            response.json()
        )

    def test_update_user_data(self):
        url = reverse('api:user-profile')
        response = self.client.put(url)
        self.assertEqual(
            status.HTTP_401_UNAUTHORIZED,
            response.status_code,
        )

        user = User.objects.create_user(
            username="test@gmail.com",
            email="test@gmail.com",
            password="Pass123@",
            first_name="Testildo",
            last_name="Tester",
            phone="11981239322",
        )

        self.client.force_authenticate(user=user)
        response = self.client.put(url, {
            "first_name": "Master",
            "last_name": "teste",
            "phone": "15999999999"
        })
        self.assertEqual(
            status.HTTP_200_OK,
            response.status_code,
        )
        User.objects.get(
            pk=user.pk,
            first_name="Master",
            last_name="teste",
            phone="15999999999",
        )


if __name__ == '__main__':
    import sys
    sys.argv = [
        '',
        'test',
        '--keepdb',
        'api.views.tests.test_user.TestUserView'
    ]
    execute_from_command_line(sys.argv)
