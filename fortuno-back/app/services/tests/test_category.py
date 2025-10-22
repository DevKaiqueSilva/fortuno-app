import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fortuno.settings')
django.setup()

from decimal import Decimal
from django.test import TestCase
from app.models.user import User
from app.models.wallet import WalletAccount, Transaction
from app.models.category import Category
from app.services.category import CategoryService

class TestCategoryService(TestCase):
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
            name='User Category',
        )
        self.category_2 = Category.objects.create(
            user=self.user,
            name='User Category 2',
        )
        self.default_category = Category.objects.create(
            user=None,
            name='Default Category',
            default_platform=True,
        )

    def test_get_dashboard_no_transactions(self):
        service = CategoryService(self.user)
        result = service.get_dashboard()
        
        self.assertEqual(result.count(), 0)

    def test_get_dashboard_with_transactions(self):
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
            category=self.default_category,
            type=Transaction.TransactionType.DEBIT,
            value=Decimal('50.00')
        )

        service = CategoryService(self.user)
        result = service.get_dashboard()
        
        self.assertEqual(result.count(), 2)
        
        user_category = result.get(name='User Category')
        self.assertEqual(user_category.total_debit, Decimal('100.00'))
        
        default_category = result.get(name='Default Category')
        self.assertEqual(default_category.total_debit, Decimal('50.00'))

    def test_get_dashboard_with_wallet_filter(self):
        wallet2 = WalletAccount.objects.create(
            user=self.user,
            name='Test Wallet 2',
            type=WalletAccount.WalletAccountType.BANK,
        )
        
        Transaction.objects.create(
            user=self.user,
            wallet_account=self.wallet,
            category=self.category,
            type=Transaction.TransactionType.DEBIT,
            value=Decimal('100.00')
        )
        Transaction.objects.create(
            user=self.user,
            wallet_account=wallet2,
            category=self.category,
            type=Transaction.TransactionType.DEBIT,
            value=Decimal('50.00')
        )

        service = CategoryService(self.user)
        result = service.get_dashboard(wallet_account=self.wallet)
        
        self.assertEqual(result.count(), 1)
        category = result.first()
        self.assertEqual(category.name, 'User Category')

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    import sys
    sys.argv = [
        '',
        'test',
        '--keepdb',
        'app.services.tests.test_category.TestCategoryService'
    ]
    execute_from_command_line(sys.argv)