from django.db import migrations
from django.contrib.auth.hashers import make_password
from decimal import Decimal
import uuid
from datetime import datetime, date
from django.utils import timezone


def create_test_data(apps, schema_editor):
    User = apps.get_model('app', 'User')
    WalletAccount = apps.get_model('app', 'WalletAccount')
    Transaction = apps.get_model('app', 'Transaction')
    Category = apps.get_model('app', 'Category')
    
    # Create test user
    user = User.objects.create(
        username='testapp@gmail.com',
        email='testapp@gmail.com',
        password=make_password('Test123@'),
        first_name='Testildo',
        last_name='Tester'
    )
    
    # Get categories
    salary_cat = Category.objects.filter(name='Salário').first()
    energy_cat = Category.objects.filter(name='Energia').first()
    food_cat = Category.objects.filter(name='Alimentação').first()
    transport_cat = Category.objects.filter(name='Transporte').first()
    shopping_cat = Category.objects.filter(name='Compras').first()
    
    # Create FortunoBank (bank account)
    bank_account = WalletAccount.objects.create(
        name='FortunoBank',
        type='bank',
        user=user
    )
    
    # Create 3 credit transactions (salary)
    Transaction.objects.create(
        name='Salário Agosto',
        value=Decimal('8000.00'),
        type='credit',
        status='paid',
        originated_at=timezone.make_aware(datetime(2025, 8, 5, 12, 0, 0)),
        wallet_account=bank_account,
        category=salary_cat,
        user=user
    )
    
    Transaction.objects.create(
        code=str(uuid.uuid4()),
        name='Salário Setembro',
        value=Decimal('8000.00'),
        type='credit',
        status='confirmed',
        originated_at=timezone.make_aware(datetime(2025, 9, 5, 12, 0, 0)),
        wallet_account=bank_account,
        category=salary_cat,
        user=user
    )
    
    Transaction.objects.create(
        name='Salário Outubro',
        value=Decimal('8000.00'),
        type='credit',
        status='paid',
        originated_at=timezone.make_aware(datetime(2025, 10, 5, 12, 0, 0)),
        wallet_account=bank_account,
        category=salary_cat,
        user=user
    )
    
    # Create 7 debit transactions (daily expenses)
    debit_transactions = [
        ('Conta de Energia', Decimal('180.50'), energy_cat, timezone.make_aware(datetime(2025, 9, 15, 12, 0, 0))),
        ('Supermercado', Decimal('320.80'), food_cat, timezone.make_aware(datetime(2025, 10, 18, 12, 0, 0))),
        ('Combustível', Decimal('150.00'), transport_cat, timezone.make_aware(datetime(2025, 8, 20, 12, 0, 0))),
        ('Farmácia', Decimal('85.30'), shopping_cat, timezone.make_aware(datetime(2025, 10, 22, 12, 0, 0))),
        ('Restaurante', Decimal('95.00'), food_cat, timezone.make_aware(datetime(2025, 10, 25, 12, 0, 0))),
        ('Uber', Decimal('25.50'), transport_cat, timezone.make_aware(datetime(2025, 9, 28, 12, 0, 0))),
        ('Conta de Água', Decimal('75.20'), energy_cat, timezone.make_aware(datetime(2025, 9, 30, 12, 0, 0)))
    ]
    
    for name, value, category, originated_at in debit_transactions:
        Transaction.objects.create(
            name=name,
            value=value,
            type='debit',
            originated_at=originated_at,
            wallet_account=bank_account,
            category=category,
            user=user
        )
    
    # Create FortCard (credit card)
    credit_card = WalletAccount.objects.create(
        name='FortCard',
        type='credit_card',
        credit_card_limit=Decimal('15000.00'),
        credit_card_expiration_day=29,
        credit_card_close_day=25,
        user=user
    )
    
    # Create 20 credit card transactions (June to October 2025)
    credit_transactions = [
        ('Netflix', Decimal('29.90'), food_cat, timezone.make_aware(datetime(2025, 6, 5, 12, 0, 0))),
        ('Supermercado Extra', Decimal('245.80'), food_cat, timezone.make_aware(datetime(2025, 6, 8, 12, 0, 0))),
        ('Posto Shell', Decimal('180.00'), transport_cat, timezone.make_aware(datetime(2025, 6, 12, 12, 0, 0))),
        ('Amazon', Decimal('89.99'), shopping_cat, timezone.make_aware(datetime(2025, 6, 15, 12, 0, 0))),
        ('Restaurante Japonês', Decimal('125.50'), food_cat, timezone.make_aware(datetime(2025, 6, 18, 12, 0, 0))),
        ('Farmácia Droga Raia', Decimal('67.30'), shopping_cat, timezone.make_aware(datetime(2025, 7, 2, 12, 0, 0))),
        ('Uber Eats', Decimal('45.80'), food_cat, timezone.make_aware(datetime(2025, 7, 5, 12, 0, 0))),
        ('Shopping Center', Decimal('320.00'), shopping_cat, timezone.make_aware(datetime(2025, 7, 10, 12, 0, 0))),
        ('Cinema', Decimal('38.00'), food_cat, timezone.make_aware(datetime(2025, 7, 14, 12, 0, 0))),
        ('Mercado Livre', Decimal('156.90'), shopping_cat, timezone.make_aware(datetime(2025, 7, 18, 12, 0, 0))),
        ('Padaria', Decimal('25.50'), food_cat, timezone.make_aware(datetime(2025, 8, 3, 12, 0, 0))),
        ('Posto Ipiranga', Decimal('195.00'), transport_cat, timezone.make_aware(datetime(2025, 8, 7, 12, 0, 0))),
        ('Livraria', Decimal('78.90'), shopping_cat, timezone.make_aware(datetime(2025, 8, 12, 12, 0, 0))),
        ('Delivery Pizza', Decimal('52.00'), food_cat, timezone.make_aware(datetime(2025, 8, 16, 12, 0, 0))),
        ('Loja de Roupas', Decimal('289.90'), shopping_cat, timezone.make_aware(datetime(2025, 8, 20, 12, 0, 0))),
        ('Spotify', Decimal('19.90'), food_cat, timezone.make_aware(datetime(2025, 9, 1, 12, 0, 0))),
        ('Supermercado Pão de Açúcar', Decimal('198.70'), food_cat, timezone.make_aware(datetime(2025, 9, 8, 12, 0, 0))),
        ('Estacionamento', Decimal('15.00'), transport_cat, timezone.make_aware(datetime(2025, 10, 15, 12, 0, 0))),
        ('Eletrônicos', Decimal('450.00'), shopping_cat, timezone.make_aware(datetime(2025, 10, 5, 12, 0, 0))),
        ('Cafeteria', Decimal('28.50'), food_cat, timezone.make_aware(datetime(2025, 10, 12, 12, 0, 0)))
    ]
    
    for name, value, category, originated_at in credit_transactions:
        Transaction.objects.create(
            name=name,
            value=value,
            type='debit',  # Credit card transactions are debit type
            originated_at=originated_at,
            wallet_account=credit_card,
            category=category,
            user=user
        )


def reverse_test_data(apps, schema_editor):
    User = apps.get_model('app', 'User')
    User.objects.filter(email='testapp@gmail.com').delete()


class Migration(migrations.Migration):
    dependencies = [
        ('app', '0005_create_default_categories'),
    ]

    operations = [
        migrations.RunPython(create_test_data, reverse_test_data),
    ]