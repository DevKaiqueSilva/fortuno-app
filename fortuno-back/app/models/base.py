import uuid
from django.db import models

class OwnedByUser(models.Model):
    code = models.UUIDField(
        editable=False,
        unique=True,
        default=uuid.uuid4,
        db_index=True,
    )
    user = models.ForeignKey(
        'app.User', 
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
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
    )
    deleted_by = models.ForeignKey(
        'app.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_deleted_by",
    )

    """
    Abstract base class for models that are owned by a user.
    Provides a foreign key relationship to the User model.
    """
    class Meta:
        abstract = True
        ordering = ['-created']