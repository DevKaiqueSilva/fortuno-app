import json
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fortuno.settings')
django.setup()

from django.utils import timezone
from django.core.management import execute_from_command_line
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from app.models.user import User
from app.models.category import Category
from app.models.wallet import Transaction, WalletAccount
from decimal import Decimal

class TestWalletView(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test@gmail.com',
            email='test@gmail.com',
            password='Pssw123@',
        )

    def test_list(self):
        Category.objects.all().delete()
        URL = reverse('api:category-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            {
                "count": 0,
                "next": None,
                "previous": None,
                "results": [],
                "pagesNumber": 1,
                "pageSize": 10
            },
            response.json()
        )
        category = Category.objects.create(
            user=self.user,
            name="Casa",
            icon="home",
            color="blue",
            default_platform=False,
        )
        response = self.client.get(URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "code": str(category.code),
                        "name": "Casa",
                        "icon": "home",
                        "color": "blue",
                        "defaultPlatform": False,
                    }
                ],
                "pagesNumber": 1,
                "pageSize": 10
            },
            response.json()
        )
        category_default = Category.objects.create(
            user=None,
            name="Saude",
            icon="health",
            color="red",
            default_platform=True,
        )
        response = self.client.get(URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            {
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "code": str(category.code),
                        "name": "Casa",
                        "icon": "home",
                        "color": "blue",
                        "defaultPlatform": False,
                    },
                    {
                        "code": str(category_default.code),
                        "name": "Saude",
                        "icon": "health",
                        "color": "red",
                        "defaultPlatform": True,
                    }
                ],
                "pagesNumber": 1,
                "pageSize": 10
            },
            response.json()
        )

    def test_create(self):
        URL = reverse('api:category-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(URL, {
            "name": "Casa",
            "icon": "home",
            "color": "blue",
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            {
                "code": response.json()['code'],
                "name": "Casa",
                "icon": "home",
                "color": "blue",
                "defaultPlatform": False,
            },
            response.json()
        )
        Category.objects.get(
            code=response.json()['code'],
            user=self.user,
            name="Casa",
            icon="home",
            color="blue",
            default_platform=False,
        )

    def test_update(self):
        category = Category.objects.create(
            user=self.user,
            name="Casa",
            icon="home",
            color="blue",
            default_platform=False,
        )
        URL = reverse('api:category-detail', args=(category.code,))
        self.client.force_authenticate(user=self.user)
        response = self.client.put(URL, {
            "name": "Restaurante",
            "icon": "rest",
            "color": "red",
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            {
                "code": str(category.code),
                "name": "Restaurante",
                "icon": "rest",
                "color": "red",
                "defaultPlatform": False,
            },
            response.json()
        )

    def test_retrieve(self):
        category = Category.objects.create(
            user=self.user,
            name="Casa",
            icon="home",
            color="blue",
            default_platform=False,
        )
        URL = reverse('api:category-detail', args=(category.code,))
        self.client.force_authenticate(user=self.user)
        response = self.client.get(URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            {
                "code": str(category.code),
                "name": "Casa",
                "icon": "home",
                "color": "blue",
                "defaultPlatform": False,
            },
            response.json()
        )

    def test_destroy(self):
        category = Category.objects.create(
            user=self.user,
            name="Casa",
            icon="home",
            color="blue",
            default_platform=False,
        )
        URL = reverse('api:category-detail', args=(category.code,))
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_dashboard(self):
        wallet = WalletAccount.objects.create(
            user=self.user,
            name="Carteira",
            type=WalletAccount.WalletAccountType.BANK,
        )
        category = Category.objects.create(
            user=self.user,
            name="Casa",
            icon="home",
            color="blue",
            default_platform=False,
        )
        category_default = Category.objects.create(
            name="Restaurante",
            icon="rest",
            color="red",
            default_platform=True,
        )
        Transaction.objects.create(
            user=self.user,
            category=category,
            value=Decimal('100'),
            wallet_account=wallet,
            type=Transaction.TransactionType.DEBIT,
        )
        Transaction.objects.create(
            user=self.user,
            category=category_default,
            value=Decimal('50'),
            wallet_account=wallet,
            type=Transaction.TransactionType.DEBIT,
        )
        Transaction.objects.create(
            user=self.user,
            category=category_default,
            value=Decimal('75'),
            wallet_account=wallet,
            type=Transaction.TransactionType.DEBIT,
        )
        URL = reverse('api:category-dashboard')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            [
                {
                    "code": str(category_default.code),
                    "name": "Restaurante",
                    "icon": "rest",
                    "color": "red",
                    "totalDebit": 12500,
                    "totalCredit": 0,
                },
                {
                    "code": str(category.code),
                    "name": "Casa",
                    "icon": "home",
                    "color": "blue",
                    "totalDebit": 10000,
                    "totalCredit": 0,
                },
            ],
            response.json()
        )


if __name__ == '__main__':
    import sys
    sys.argv = [
        '',
        'test',
        '--keepdb',
        'api.views.tests.test_category.TestWalletView'
    ]
    execute_from_command_line(sys.argv)
