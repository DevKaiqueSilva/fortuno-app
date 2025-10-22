from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from app.models.user import User
from app.utils import decimal_to_cents

class UserSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'phone',
            'created',
            'balance',
        )

    def get_balance(self, instance):
        from app.services.balance import BalanceService
        balance = BalanceService(instance).get_balance()
        return dict(
            total_debit=decimal_to_cents(balance["total_debit"] or 0),
            total_credit=decimal_to_cents(balance["total_credit"] or 0)
        )

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'phone',
        )

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance
    
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'phone',
            'password',
        )
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8,
            }
        }

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        validated_data["username"] = validated_data["email"]
        return User.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(
        trim_whitespace=False,
        max_length=128,
        write_only=True,
    )

    def validate(self, attrs):
        data = super().validate(attrs)
        username = data.get('email')
        password = data.get('password')

        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username, 
                password=password,
            )
        data['user'] = user
        return data