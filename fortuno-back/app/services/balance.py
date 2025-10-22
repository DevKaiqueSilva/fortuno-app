from typing import Optional
from app.models import User, Transaction, WalletAccount
from django.db.models import Sum, Q

class BalanceService:
    def __init__(self, user: User):
        self.user = user

    def get_balance(self, wallet_account: Optional[WalletAccount] = None):
        queryset = Transaction.objects.filter(
            user=self.user
        )
        if wallet_account:
            queryset = queryset.filter(wallet_account=wallet_account)
        return queryset.aggregate(
            total_debit=-Sum('value', filter=Q(type='debit')),
            total_credit=Sum('value', filter=Q(type='credit'))
        )