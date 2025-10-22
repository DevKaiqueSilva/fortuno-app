from app.utils import decimal_to_cents, cents_to_decimal
from rest_framework import serializers


class MoneyField(serializers.DecimalField):
    def to_representation(self, value):
        return decimal_to_cents(value)

    def to_internal_value(self, data):
        return cents_to_decimal(data)