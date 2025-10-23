import json
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fortuno.settings')
django.setup()

from decimal import Decimal
from django.utils import timezone
from django.core.management import execute_from_command_line
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from app.models.user import User
from app.models.wallet import WalletAccount, Transaction
from app.models.category import Category
from freezegun import freeze_time

class TestTransactionView(APITestCase):
    maxDiff = None

    def setUp(self):
        self.user = User.objects.create_user(
            username='test@gmail.com',
            email='test@gmail.com',
            password='Pssw123@',
        )
        self.wallet = WalletAccount.objects.create(
            user=self.user,
            name='Nubank',
            type=WalletAccount.WalletAccountType.BANK,
        )
        self.category = Category.objects.create(
            user=self.user,
            name='Alimentacao',
        )
        self.category_2 = Category.objects.create(
            user=self.user,
            name='Transporte',
        )

    @freeze_time("2025-08-02 15:15:00")
    def test_list(self):
        URL = reverse('api:transactions-list')
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
        transaction = Transaction.objects.create(
            user=self.user,
            wallet_account=self.wallet,
            category=self.category,
            description='Supermercado',
            type=Transaction.TransactionType.DEBIT,
            status=Transaction.TransactionStatus.PAID,
            value=Decimal('100'),
            originated_at=timezone.now(),
        )
        response = self.client.get(URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            {
                "count":  1,
                "next":  None,
                "previous":  None,
                "results":  [
                    {
                        "code": str(transaction.code),
                        "name": "",
                        "value": 10000,
                        "type": "debit",
                        "status": "paid",
                        "originatedAt": "2025-08-02T15:15:00Z",
                        "description": "Supermercado",
                        "installmentsEnabled": False,
                        "installments": 1,
                        "currentInstallment": 1,
                        "walletAccount": {
                            "code": str(self.wallet.code),
                            "name": "Nubank",
                            "type": "bank",
                            "creditCardLimit": 0,
                            "creditCardExpirationDay": 0,
                            "creditCardCloseDay": 0,
                            "balance": {"totalCredit": 0, "totalDebit": -10000},
                        },
                        "category": {
                            "code": str(self.category.code),
                            "name": "Alimentacao",
                            "icon": "",
                            "color": "",
                            "defaultPlatform": False
                        }
                    }
                ],
                "pagesNumber": 1,
                "pageSize": 10
            },
            response.json()
        )

        response = self.client.get(URL+f'?category_code={str(self.category_2.code)}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([], response.json()["results"])
    
    @freeze_time("2025-08-02 15:15:00")
    def test_retrieve(self):
        transaction = Transaction.objects.create(
            user=self.user,
            wallet_account=self.wallet,
            category=self.category,
            description='Supermercado',
            type=Transaction.TransactionType.DEBIT,
            status=Transaction.TransactionStatus.PAID,
            value=Decimal('100'),
            originated_at=timezone.now(),
        )
        URL = reverse('api:transactions-detail', args=(transaction.code,))
        self.client.force_authenticate(user=self.user)
        response = self.client.get(URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            {
                "code": str(transaction.code),
                "name": "",
                "value": 10000,
                "type": "debit",
                "status": "paid",
                "originatedAt": "2025-08-02T15:15:00Z",
                "description": "Supermercado",
                "installmentsEnabled": False,
                "installments": 1,
                "currentInstallment": 1,
                "walletAccount": {
                    "code": str(self.wallet.code),
                    "name": "Nubank",
                    "type": "bank",
                    "creditCardLimit": 0,
                    "creditCardExpirationDay": 0,
                    "creditCardCloseDay": 0,
                    "balance": {"totalCredit": 0, "totalDebit": -10000},
                },
                "category": {
                    "code": str(self.category.code),
                    "name": "Alimentacao",
                    "icon": "",
                    "color": "",
                    "defaultPlatform": False
                }
            },
            response.json()
        )
    
    @freeze_time("2025-08-02 16:15:00")
    def test_create(self):
        URL = reverse('api:transactions-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            URL, 
            data=json.dumps({
                "name": "Pagamento",
                "value": 5000,
                "type": "debit",
                "status": "paid",
                "originatedAt": "2025-08-02T16:15:00Z",
                "description": "Supermercado",
                "installmentsEnabled": False,
                "installments": 1,
                "currentInstallment": 1,
                "categoryCode": str(self.category.code),
                "walletAccountCode": str(self.wallet.code),
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            {
                "code": response.json()["code"],
                "name": "Pagamento",
                "value": 5000,
                "type": "debit",
                "status": "paid",
                "originatedAt": "2025-08-02T16:15:00Z",
                "description": "Supermercado",
                "installmentsEnabled": False,
                "installments": 1,
                "currentInstallment": 1,
                "walletAccount": {
                    "code": str(self.wallet.code),
                    "name": "Nubank",
                    "type": "bank",
                    "creditCardLimit": 0,
                    "creditCardExpirationDay": 0,
                    "creditCardCloseDay": 0,
                    "balance": {"totalCredit": 0, "totalDebit": -5000},
                },
                "category": {
                    "code": str(self.category.code),
                    "name": "Alimentacao",
                    "icon": "",
                    "color": "",
                    "defaultPlatform": False
                }
            },
            response.json()
        )
        Transaction.objects.get(
            code=response.json()['code'],
            user=self.user,
            description='Supermercado',
            type=Transaction.TransactionType.DEBIT,
            status=Transaction.TransactionStatus.PAID,
            value=Decimal('50.00'),
            category=self.category,
            wallet_account=self.wallet,
        )

    @freeze_time("2025-08-02 16:15:00")
    def test_update(self):
        transaction = Transaction.objects.create(
            user=self.user,
            wallet_account=self.wallet,
            category=self.category,
            description='Supermercado',
            type=Transaction.TransactionType.DEBIT,
            status=Transaction.TransactionStatus.PAID,
            value=Decimal('100'),
            originated_at=timezone.now(),
        )
        URL = reverse('api:transactions-detail', args=(transaction.code,))
        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            URL, 
            data=json.dumps({
                "name": "Combustivel",
                "value": 15000,
                "type": "debit",
                "status": "paid",
                "originatedAt": "2025-08-02T16:15:00Z",
                "description": "xxx",
                "installmentsEnabled": True,
                "installments": 1,
                "currentInstallment": 1,
                "categoryCode": str(self.category.code),
                "walletAccountCode": str(self.wallet.code),
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            {
                "code": response.json()["code"],
                "name": "Combustivel",
                "value": 15000,
                "type": "debit",
                "status": "paid",
                "originatedAt": "2025-08-02T16:15:00Z",
                "description": "xxx",
                "installmentsEnabled": True,
                "installments": 1,
                "currentInstallment": 1,
                "walletAccount": {
                    "code": str(self.wallet.code),
                    "name": "Nubank",
                    "type": "bank",
                    "creditCardLimit": 0,
                    "creditCardExpirationDay": 0,
                    "creditCardCloseDay": 0,
                    "balance": {"totalCredit": 0, "totalDebit": -15000},
                },
                "category": {
                    "code": str(self.category.code),
                    "name": "Alimentacao",
                    "icon": "",
                    "color": "",
                    "defaultPlatform": False
                }
            },
            response.json()
        )
        Transaction.objects.get(
            pk=transaction.pk,
            user=self.user,
            name="Combustivel",
            description="xxx",
            type=Transaction.TransactionType.DEBIT,
            status=Transaction.TransactionStatus.PAID,
            value=Decimal('150.00'),
            category=self.category,
            wallet_account=self.wallet,
        )

    def test_destroy(self):
        transaction = Transaction.objects.create(
            user=self.user,
            wallet_account=self.wallet,
            category=self.category,
            description='Supermercado',
            type=Transaction.TransactionType.DEBIT,
            status=Transaction.TransactionStatus.PAID,
            value=Decimal('100'),
            originated_at=timezone.now(),
        )
        URL = reverse('api:transactions-detail', args=(transaction.code,))
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


if __name__ == '__main__':
    import sys
    sys.argv = [
        '',
        'test',
        '--keepdb',
        'api.views.tests.test_transaction.TestTransactionView'
    ]
    execute_from_command_line(sys.argv)
