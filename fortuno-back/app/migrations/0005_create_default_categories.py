from django.db import migrations

def create_default_categories(apps, schema_editor):
    Category = apps.get_model('app', 'Category')
    
    categories = [
        {'name': 'Alimentação', 'color': '#FF6B6B', 'icon': 'restaurant'},
        {'name': 'Restaurante', 'color': '#4ECDC4', 'icon': 'local_dining'},
        {'name': 'Saúde', 'color': '#45B7D1', 'icon': 'medical_services'},
        {'name': 'Transporte', 'color': '#96CEB4', 'icon': 'directions_car'},
        {'name': 'Lazer', 'color': '#FFEAA7', 'icon': 'sports_esports'},
        {'name': 'Estudos', 'color': '#DDA0DD', 'icon': 'school'},
        {'name': 'Pet', 'color': '#98D8C8', 'icon': 'pets'},
        {'name': 'Casa', 'color': '#F7DC6F', 'icon': 'home'},
        {'name': 'Assinatura', 'color': '#BB8FCE', 'icon': 'subscriptions'},
        {'name': 'Salário', 'color': '#85C1E9', 'icon': 'payments'},
        {'name': 'Compras', 'color': "#F410F8", 'icon': 'shopping_cart'},
        {'name': 'Energia', 'color': "#71A5F8", 'icon': 'category'},
        {'name': 'Outros', 'color': '#F8C471', 'icon': 'category'},
    ]
    
    for category_data in categories:
        Category.objects.create(
            name=category_data['name'],
            color=category_data['color'],
            icon=category_data['icon'],
            default_platform=True,
            user=None
        )

def reverse_default_categories(apps, schema_editor):
    Category = apps.get_model('app', 'Category')
    Category.objects.filter(default_platform=True).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('app', '0004_alter_transaction_originated_at'),
    ]

    operations = [
        migrations.RunPython(create_default_categories, reverse_default_categories),
    ]