from django.utils import timezone
from rest_framework.response import Response
from rest_framework.pagination import (
    PageNumberPagination, CursorPagination
)
from rest_framework import filters, mixins, status, viewsets, permissions
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'

    def get_page_size(self, request):
        page_size = request.query_params.get(self.page_size_query_param)
        if page_size is not None:
            return int(page_size)
        return self.page_size

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
            'pages_number': self.page.paginator.num_pages,
            'page_size': self.get_page_size(self.request)
        })
    
class BaseOwnedByUserModelViewSet(viewsets.ModelViewSet):
    lookup_field = 'code'
    filter_backends = (
        filters.SearchFilter,
        DjangoFilterBackend,
    )
    pagination_class = CustomPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated,]
    soft_delete = True
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        if not context:
            context = {}
        context['user'] = self.request.user
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user=self.request.user,
            deleted_at=None,
            user__isnull=False,
        )
    
    def destroy(self, request, *args, **kwargs) -> Response:
        if self.soft_delete: 
            instance = self.get_object()
            instance.deleted_at = timezone.now()
            instance.deleted_by = request.user
            instance.save()
            return Response(
                {"message": "The item has been successfully deleted"},
                status=status.HTTP_204_NO_CONTENT
            )
        
        return super().destroy(request, *args, **kwargs)
       