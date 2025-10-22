from rest_framework import viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.serializers.wallet import WalletAccountSerializer
from api.views.base import BaseOwnedByUserModelViewSet
from rest_framework.decorators import action
from app.models.wallet import WalletAccount


class WalletAccountViewSet(BaseOwnedByUserModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = WalletAccountSerializer
    queryset = WalletAccount.objects.all()