from apps.users.models import User
from apps.users.models.email_confirmation import EmailConfirmationCode
from django.core.exceptions import ValidationError

class ConfirmEmailCodeUseCase:
    def execute(self, email: str, code: str) -> None:
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("Пользователь не найден")

        try:
            confirmation = EmailConfirmationCode.objects.get(
                user=user, code=code, is_used=False
            )
        except EmailConfirmationCode.DoesNotExist:
            raise ValidationError("Неверный код или уже использован")

        if confirmation.is_expired():
            raise ValidationError("Код истек")

        user.is_active = True
        user.save()

        confirmation.is_used = True
        confirmation.save()
