from api.serializers.base import OwnedByUserModelSerializer
from app.models.wallet import WalletAccount, Transaction
from app.models.category import Category
from rest_framework import serializers
from api.serializers.category import CategorySerializer
from api.serializers.fields import MoneyField
from app.utils import decimal_to_cents

class WalletAccountSerializer(OwnedByUserModelSerializer):
    credit_card_limit = MoneyField(max_digits=10, decimal_places=2, required=False)
    balance = serializers.SerializerMethodField()
    
    class Meta:
        model = WalletAccount
        fields = (
            'code',
            'name',
            'type',
            'credit_card_limit',
            'credit_card_expiration_day',
            'credit_card_close_day',
            'balance',
        )

    def get_balance(self, instance: WalletAccount):
        from app.services.balance import BalanceService
        balance = BalanceService(instance.user).get_balance(wallet_account=instance)
        return dict(
            total_debit=decimal_to_cents(balance["total_debit"] or 0),
            total_credit=decimal_to_cents(balance["total_credit"] or 0)
        )

class TransactionSerializer(OwnedByUserModelSerializer):
    wallet_account = WalletAccountSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    value = MoneyField(max_digits=10, decimal_places=2)
    wallet_account_code = serializers.CharField(required=True, write_only=True)
    category_code = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = Transaction
        fields = (
            'code',
            'name',
            'value',
            'type',
            'status',
            'originated_at',
            'description',
            'installments_enabled',
            'installments',
            'current_installment',
            'wallet_account',
            'wallet_account_code',
            'category',
            'category_code',
        )

    def _sync_fk_data(self, validated_data):
        wallet_account_code = validated_data.pop('wallet_account_code', None)
        category_code = validated_data.pop('category_code', None)

        if wallet_account_code:
            wallet_account = WalletAccount.objects.get(code=wallet_account_code)
            validated_data['wallet_account'] = wallet_account

        if category_code:
            category = Category.objects.get(code=category_code)
            validated_data['category'] = category

    def create(self, validated_data):
        self._sync_fk_data(validated_data)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        self._sync_fk_data(validated_data)

        return super().update(instance, validated_data)