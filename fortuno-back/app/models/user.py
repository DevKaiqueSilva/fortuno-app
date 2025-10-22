from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    phone = models.CharField(
        max_length=20,
        default="",
        blank=True,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'