from rest_framework import permissions, viewsets, status, views
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenRefreshView
from api.serializers.user import (
    UserLoginSerializer,
    UserSerializer,
    UserRegisterSerializer,
    UserProfileSerializer,
)
from app.models.user import User


class UserLoginViewSet(views.APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context=dict(
                request=request,
            ),
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_data = {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "expires_at": refresh.payload["exp"],
            }

            return Response(user_data, status=status.HTTP_200_OK)
        else:
            return Response(
                data={"message": "The user e-mail or password is invalid"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
    

class UserRegisterViewSet(views.APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        if user:
            return Response(
                {"message": "User registered with success"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={"message": "Fail on create user"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        
class UserProfileViewSet(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            instance=request.user,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        if user:
            return Response(
                {"message": "User updated with success"}, 
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={"message": "Fail on update user"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class MeApiView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.data["access_token"] = response.data["access"]
        response.data.pop("access")
        response.data["refresh_token"] = response.data["refresh"]
        response.data.pop("refresh")
        return response
