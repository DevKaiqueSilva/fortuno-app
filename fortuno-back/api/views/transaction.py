from rest_framework import viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.serializers.wallet import TransactionSerializer
from api.views.base import BaseOwnedByUserModelViewSet
from app.models.wallet import Transaction
from django_filters import rest_framework as filters

class TransactionFilterView(filters.FilterSet):
    wallet_account_code = filters.CharFilter(field_name="wallet_account__code", lookup_expr="exact")
    category_code = filters.CharFilter(field_name="category__code", lookup_expr="exact")
    month = filters.NumberFilter(field_name="originated_at", lookup_expr="month")
    year = filters.NumberFilter(field_name="originated_at", lookup_expr="year")
    
    class Meta:
        model = Transaction
        fields = ["wallet_account", "category", "month", "year"]

class TransactionViewSet(BaseOwnedByUserModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = TransactionSerializer
    filterset_class = TransactionFilterView
    queryset = Transaction.objects.all()
    search_fields = ["name"]