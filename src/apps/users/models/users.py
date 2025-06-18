import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import (
    models,
    transaction,
)
from django.utils.translation import gettext_lazy as _
from social_core.utils import first

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
    password = models.CharField(max_length=128, verbose_name=_('Пароль'))

    organization = models.ForeignKey(
        to='users.Organization',
        on_delete=models.SET_NULL,
        related_name='users',
        verbose_name=_('Организация'),
        null=True,
    )

    phone = models.CharField(
        max_length=32,
        verbose_name=_('Телефон')
    )

    role = models.CharField(
        max_length=256,
        verbose_name=_('Роль'),
        choices=[(role.value, role.value) for role in UserRole]
    )
    enters_count = models.BigIntegerField(default=0, verbose_name=_('Количество входов'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    username = None

    objects = UserManager()

    def to_entity(self) -> UserEntity:
        return UserEntity(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            phone=self.phone,
            password=self.password,
            email=self.email,
            organization=self.organization.to_entity() if self.organization else None,
            is_active=self.is_active,
            role=self.role,
            enters_count=self.enters_count,
        )

    @classmethod
    def from_entity(cls, user: UserEntity):
        return cls(
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone,
            email=user.email,
            password=user.password,
            organization=user.organization if user.organization else None,
            role=user.role,
            is_active=user.is_active,
        )

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

