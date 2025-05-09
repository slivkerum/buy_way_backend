from datetime import timedelta
from django.utils import timezone
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.template.loader import render_to_string

from apps.users.models.email_confirmation import EmailConfirmationCode
from apps.users.models import User

from config.settings.base import EMAIL_HOST_USER


class SendEmailConfirmationCodeUseCase:
    def execute(self, email: str) -> None:
        user = User.objects.get(email=email)

        code = EmailConfirmationCode.generate_code()
        expires_at = timezone.now() + timedelta(minutes=10)

        EmailConfirmationCode.objects.create(
            user=user,
            code=code,
            expires_at=expires_at
        )

        self.send_confirmation_email(user, code)

    @staticmethod
    def send_confirmation_email(user: User, code: str) -> None:
        subject = "Подтверждение email"
        html_message = render_to_string(
            'send.html',
            {'user': user, 'confirmation_code': code}
        )
        plain_message = strip_tags(html_message)

        send_mail(
            subject,
            plain_message,
            EMAIL_HOST_USER,
            [user.email],
            html_message=html_message
        )

