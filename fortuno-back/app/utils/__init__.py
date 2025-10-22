from decimal import Decimal

def decimal_to_cents(decimal_number):
    return int(decimal_number * Decimal('100').quantize(Decimal('1')))

def cents_to_decimal(cents):
    return Decimal(cents)/Decimal('100.00')
