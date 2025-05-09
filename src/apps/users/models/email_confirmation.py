import random

from django.db import models
from django.utils import timezone

from apps.users.models import User


class EmailConfirmationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="confirmation_codes")
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.expires_at

    @staticmethod
    def generate_code() -> str:
        return f"{random.randint(100000, 999999)}"
