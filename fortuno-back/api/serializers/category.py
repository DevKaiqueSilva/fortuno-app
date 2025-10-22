from api.serializers.base import OwnedByUserModelSerializer
from app.models.category import Category
from api.serializers.fields import MoneyField

class CategorySerializer(OwnedByUserModelSerializer):
    class Meta:
        model = Category
        fields = (
            'code',
            'name',
            'icon',
            'color',
            'default_platform',
        )
        extra_kwargs = {
            'default_platform': {
                'read_only': True,
            }
        }

class CategoryDashboardSerializer(OwnedByUserModelSerializer):
    total_debit = MoneyField(max_digits=10, decimal_places=2)
    total_credit = MoneyField(max_digits=10, decimal_places=2)
    class Meta:
        model = Category
        fields = (
            'code',
            'name',
            'icon',
            'color',
            'total_debit',
            'total_credit',
        )