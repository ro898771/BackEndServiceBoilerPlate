import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Review(models.Model):
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 (worst) to 5 (best)",
    )
    comment = models.TextField(help_text="Comment text")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review #{self.pk} – Rating {self.rating}"


class HandshakeToken(models.Model):
    """
    One-time token used to confirm a write operation.

    Flow:
      1. Client calls POST /api/dinasour/handshake/
      2. Server creates a token and returns it  (status: ready)
      3. Client sends the actual write request with header X-Handshake-Token
      4. Server validates → marks token used → performs the operation
    """
    EXPIRY_SECONDS = 60

    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def is_valid(self):
        if self.used:
            return False
        age = (timezone.now() - self.created_at).total_seconds()
        return age <= self.EXPIRY_SECONDS

    def __str__(self):
        status = "used" if self.used else ("expired" if not self.is_valid() else "ready")
        return f"Token {self.token} [{status}]"
