from django.db import models
from app.models.base import OwnedByUser

class Category(OwnedByUser):
    name = models.CharField(
        max_length=120,
    )
    icon = models.CharField(
        max_length=30,
        default="",
        blank=True,
    )
    color = models.CharField(
        max_length=30,
        default="",
        blank=True,
    )
    default_platform = models.BooleanField(
        default=False
    )