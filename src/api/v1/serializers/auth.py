from rest_framework import serializers

from apps.users.entities.users import UserRole
from apps.users.use_cases.register_user import RegisterUserUseCase
from config.containers import get_container


class RegisterSerializer(serializers.Serializer):
    container = get_container()
    register_user: RegisterUserUseCase = container.resolve(RegisterUserUseCase)

    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone = serializers.CharField(required=True)
    role = serializers.ChoiceField(choices=[(role.name, role.value) for role in UserRole], required=True)

    @staticmethod
    def validate_role(value):
        try:
            return UserRole[value].value
        except KeyError:
            raise serializers.ValidationError("Некорректная роль пользователя")

    def create(self, validated_data):
        return self.register_user.execute(validated_data)
