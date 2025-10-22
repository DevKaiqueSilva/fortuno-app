from app.models import User, Category, Transaction, WalletAccount
from django.db.models import Q
from django.db.models import Sum
from typing import Optional
from django.db.models.functions import Coalesce
from decimal import Decimal

class CategoryService:
    def __init__(self, user: User):
        self.user = user

    def get_dashboard(self, wallet_account: Optional[WalletAccount] = None):
        queryset = Category.objects.filter(
            Q(user=self.user) 
            | 
            Q(default_platform=True)
        )
        if wallet_account:
            queryset = queryset.filter(
                Q(transactions__wallet_account=wallet_account)
            ).distinct()
        return queryset.annotate(
            total_debit=Coalesce(Sum(
                'transactions__value', 
                filter=Q(transactions__type=Transaction.TransactionType.DEBIT, transactions__user=self.user),
                distinct=True,
            ), Decimal('0')),
            total_credit=Coalesce(Sum(
                'transactions__value', 
                filter=Q(transactions__type=Transaction.TransactionType.CREDIT, transactions__user=self.user),
                distinct=True,
            ), Decimal('0'))
        ).filter(
            total_debit__gt=0,
        ).order_by('-total_debit')