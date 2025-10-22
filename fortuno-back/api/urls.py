from django.urls import include, path
from rest_framework import routers

from api.views.user import (
    UserLoginViewSet, UserRegisterViewSet, MeApiView, UserProfileViewSet
)
from api.views.wallet import (
    WalletAccountViewSet,
)
from api.views.category import (
    CategoryViewSet,
)
from api.views.transaction import (
    TransactionViewSet,
)

router = routers.DefaultRouter()

router.register(
    r'wallet', 
    viewset=WalletAccountViewSet, 
    basename='wallet'
)
router.register(
    r'category', 
    viewset=CategoryViewSet, 
    basename='category'
)
router.register(
    r'transactions', 
    viewset=TransactionViewSet, 
    basename='transactions'
)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('user/login/', UserLoginViewSet.as_view(), name="user-login"),
    path('user/profile/', UserProfileViewSet.as_view(), name="user-profile"),
    path('user/register/', UserRegisterViewSet.as_view(), name="user-register"),
    path('user/me/', MeApiView.as_view(), name="user-me"),
    path('', include(router.urls)),
]