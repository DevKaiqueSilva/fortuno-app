import uuid
from django.db import models
from app.models.user import User

class OwnedByUser(models.Model):
    code = models.UUIDField(
        editable=False,
        unique=True,
        default=uuid.uuid4,
        db_index=True,
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        null=True,
        default=None
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    """
    Abstract base class for models that are owned by a user.
    Provides a foreign key relationship to the User model.
    """
    class Meta:
        abstract = True