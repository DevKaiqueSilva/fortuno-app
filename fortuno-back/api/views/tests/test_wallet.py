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
from app.models.wallet import WalletAccount, Transaction
from decimal import Decimal


class TestWalletView(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test@gmail.com',
            email='test@gmail.com',
            password='Pssw123@',
        )

    def test_list(self):
        URL = reverse('api:wallet-list')
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

        wallet = WalletAccount.objects.create(
            user=self.user,
            name='Nubank',
            type=WalletAccount.WalletAccountType.BANK,
        )
        wallet_deleted = WalletAccount.objects.create(
            user=self.user,
            name='Itau',
            type=WalletAccount.WalletAccountType.BANK,
            deleted_at=timezone.now(),
        )
        wallet_from_another_user = WalletAccount.objects.create(
            user=User.objects.create_user(
                username='test2@gmail.com',
                email='test2@gmail.com',
                password='Pssw123@',
            ),
            name='Nubank',
            type=WalletAccount.WalletAccountType.BANK,
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
                        "code": str(wallet.code),
                        "name": "Nubank",
                        "type": "bank",
                        "creditCardLimit": 0,
                        "creditCardExpirationDay": 0,
                        "creditCardCloseDay": 0,
                        "balance": {
                            "totalDebit": 0,
                            "totalCredit": 0,
                        }
                    }
                ],
                "pagesNumber": 1,
                "pageSize": 10
            },
            response.json()
        )

    def test_create(self):
        URL = reverse('api:wallet-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(URL, {
            'name': 'Nubank',
            'type': 'bank',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            {
                "code": response.json()['code'],
                "name": "Nubank",
                "type": "bank",
                "creditCardLimit": 0,
                "creditCardExpirationDay": 0,
                "creditCardCloseDay": 0,
                "balance": {
                    "totalDebit": 0,
                    "totalCredit": 0,
                }
            },
            response.json()
        )
        WalletAccount.objects.get(
            code=response.json()['code'],
            name='Nubank',
            type=WalletAccount.WalletAccountType.BANK,
            user=self.user
        )

    def test_update(self):
        wallet = WalletAccount.objects.create(
            user=self.user,
            name='Nubank',
            type=WalletAccount.WalletAccountType.BANK,
        )
        URL = reverse('api:wallet-detail', args=(wallet.code,))
        self.client.force_authenticate(user=self.user)
        response = self.client.put(URL, {
            'name': 'Itau',
            'type': 'bank',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            {
                "code": str(wallet.code),
                "name": "Itau",
                "type": "bank",
                "creditCardLimit": 0,
                "creditCardExpirationDay": 0,
                "creditCardCloseDay": 0,
                "balance": {
                    "totalDebit": 0,
                    "totalCredit": 0,
                }
            },
            response.json()
        )

    def test_retrieve(self):
        wallet = WalletAccount.objects.create(
            user=self.user,
            name='Nubank',
            type=WalletAccount.WalletAccountType.BANK,
        )
        Transaction.objects.create(
            user=self.user,
            value=Decimal('100'),
            type=Transaction.TransactionType.CREDIT,
            wallet_account=wallet,
        )
        Transaction.objects.create(
            user=self.user,
            value=Decimal('75'),
            type=Transaction.TransactionType.DEBIT,
            wallet_account=wallet,
        )
        URL = reverse('api:wallet-detail', args=(wallet.code,))
        self.client.force_authenticate(user=self.user)
        response = self.client.get(URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            {
                "code": response.json()['code'],
                "name": "Nubank",
                "type": "bank",
                "creditCardLimit": 0,
                "creditCardExpirationDay": 0,
                "creditCardCloseDay": 0,
                "balance": {
                    "totalDebit": -7500,
                    "totalCredit": 10000,
                }
            },
            response.json()
        )

    def test_destroy(self):
        wallet = WalletAccount.objects.create(
            user=self.user,
            name='Nubank',
            type=WalletAccount.WalletAccountType.BANK,
        )
        URL = reverse('api:wallet-detail', args=(wallet.code,))
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


if __name__ == '__main__':
    import sys
    sys.argv = [
        '',
        'test',
        '--keepdb',
        'api.views.tests.test_wallet.TestWalletView'
    ]
    execute_from_command_line(sys.argv)
