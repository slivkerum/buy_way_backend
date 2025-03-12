import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import (
    models,
    transaction,
)
from django.utils.translation import gettext_lazy as _

from apps.users.entities.users import (
    UserEntity,
    UserRole,
)


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        with transaction.atomic():
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save()
            return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    first_name = models.CharField(max_length=256, verbose_name=_('Имя'))
    last_name = models.CharField(max_length=256, verbose_name=_('Фамилия'))

    email = models.EmailField(unique=True, verbose_name=_('Email'))
    role = models.CharField(
        max_length=256,
        verbose_name=_('Роль'),
        choices=[(role.value, role.value) for role in UserRole]
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    username = None

    objects = UserManager()

    def to_entity(self) -> UserEntity:
        return UserEntity(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            password=self.password,
            email=self.email,
            role=self.role,
        )

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

