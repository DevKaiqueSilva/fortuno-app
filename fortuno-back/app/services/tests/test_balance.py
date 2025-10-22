import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fortuno.settings')
django.setup()

from decimal import Decimal
from django.test import TestCase
from app.models.user import User
from app.models.wallet import WalletAccount, Transaction
from app.models.category import Category
from app.services.balance import BalanceService

class TestBalanceService(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test@gmail.com',
            email='test@gmail.com',
            password='Pssw123@',
        )
        self.wallet = WalletAccount.objects.create(
            user=self.user,
            name='Test Wallet',
            type=WalletAccount.WalletAccountType.BANK,
        )
        self.category = Category.objects.create(
            user=self.user,
            name='Test Category',
        )

    def test_get_balance_no_transactions(self):
        service = BalanceService(self.user)
        result = service.get_balance()
        
        self.assertEqual(result['total_debit'], None)
        self.assertEqual(result['total_credit'], None)

    def test_get_balance_with_transactions(self):
        Transaction.objects.create(
            user=self.user,
            wallet_account=self.wallet,
            category=self.category,
            type=Transaction.TransactionType.DEBIT,
            value=Decimal('100.00')
        )
        Transaction.objects.create(
            user=self.user,
            wallet_account=self.wallet,
            category=self.category,
            type=Transaction.TransactionType.CREDIT,
            value=Decimal('50.00')
        )
        Transaction.objects.create(
            user=self.user,
            wallet_account=self.wallet,
            category=self.category,
            type=Transaction.TransactionType.DEBIT,
            value=Decimal('25.00')
        )

        service = BalanceService(self.user)
        result = service.get_balance()
        
        self.assertEqual(result['total_debit'], Decimal('-125.00'))
        self.assertEqual(result['total_credit'], Decimal('50.00'))

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    import sys
    sys.argv = [
        '',
        'test',
        '--keepdb',
        'app.services.tests.test_balance.TestBalanceService'
    ]
    execute_from_command_line(sys.argv)