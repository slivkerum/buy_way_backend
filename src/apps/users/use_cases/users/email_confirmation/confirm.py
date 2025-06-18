from apps.users.exceptions.users import CodeIstek, InvalidCode, UserEmailNotFound
from apps.users.models import User
from apps.users.models.email_confirmation import EmailConfirmationCode
from django.core.exceptions import ValidationError

class ConfirmEmailCodeUseCase:
    def execute(self, email: str, code: str) -> None:
        try:
            user = User.objects.filter(email=email).first()
        except User.DoesNotExist:
            raise UserEmailNotFound(email=email)

        try:
            confirmation = EmailConfirmationCode.objects.get(
                user=user, code=code, is_used=False
            )
        except EmailConfirmationCode.DoesNotExist:
            raise InvalidCode()

        if confirmation.is_expired():
            raise CodeIstek()

        user.is_active = True
        user.save()

        confirmation.is_used = True
        confirmation.save()
