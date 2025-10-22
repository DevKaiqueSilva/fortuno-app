from rest_framework import viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.serializers.category import CategorySerializer, CategoryDashboardSerializer
from api.views.base import BaseOwnedByUserModelViewSet
from rest_framework.response import Response

from app.models.category import Category
from rest_framework.decorators import action
from app.services.category import CategoryService


class CategoryViewSet(BaseOwnedByUserModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_queryset(self):
        platform_queryset = Category.objects.filter(default_platform=True)
        queryset = super().get_queryset() 
        return (queryset | platform_queryset).distinct().order_by("name")
    
    @action(detail=False, methods=["GET"])
    def dashboard(self, request):
        queryset = CategoryService(user=request.user).get_dashboard()
        serializer = CategoryDashboardSerializer(queryset, many=True)
        return Response(serializer.data)