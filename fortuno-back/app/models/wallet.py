from django.db import models
from decimal import Decimal
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

from app.models.base import OwnedByUser

class WalletAccount(OwnedByUser):
    class WalletAccountType(models.TextChoices):
        BANK = "bank"
        CREDIT_CARD = "credit_card"
        INVESTMENT = "investment"

    name = models.CharField(
        max_length=120,
    )
    type = models.CharField(
        max_length=30,
        choices=WalletAccountType.choices,
        default=WalletAccountType.BANK,
    )
    credit_card_limit = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0")
    )
    credit_card_expiration_day = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(30)],
        default=0
    )
    credit_card_close_day = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(30)],
        default=0
    )

    def __str__(self):
        return f"{self.name} - {self.type}"
    
class Transaction(OwnedByUser):
    class TransactionType(models.TextChoices):
        CREDIT = "credit"
        DEBIT = "debit"

    class TransactionStatus(models.TextChoices):
        PENDING = "pending"
        CANCELED = "canceled"
        PAID = "paid"
        DRAFT = "draft"

    name = models.CharField(
        max_length=120,
        blank=True,
        default="",
    )
    value = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0")
    )
    type = models.CharField(
        max_length=30,
        choices=TransactionType.choices,
        default=TransactionType.DEBIT,
    )
    status = models.CharField(
        max_length=30,
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING,
    )
    originated_at = models.DateTimeField(
        null=True,
        default=None,
    )
    description = models.CharField(
        max_length=200,
        default="",
        blank=True,
    )
    installments_enabled = models.BooleanField(
        default=False
    )
    installments = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(30)],
        default=1
    )
    current_installment = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(30)],
        default=1
    )
    wallet_account = models.ForeignKey(
        WalletAccount,
        on_delete=models.CASCADE,
        related_name="transactions",
    )
    category = models.ForeignKey(
        'app.Category',
        on_delete=models.CASCADE,
        related_name="transactions",
        null=True,
        blank=True,
    )
    def __str__(self):
        return f"{self.type} - {self.value} - {self.wallet_account.name}"
    