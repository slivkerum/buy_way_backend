from rest_framework import serializers

from apps.users.entities.users import UserRole
from apps.users.use_cases.users.auth.registration import RegisterUserUseCase
from config.containers import get_container


class RegisterSerializer(serializers.Serializer):
    container = get_container()
    register_user: RegisterUserUseCase = container.resolve(RegisterUserUseCase)

    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone = serializers.CharField(required=True)
    role = serializers.ChoiceField(choices=[(role.name, role.value) for role in UserRole], required=True)

    organization_name = serializers.CharField(required=False)
    organization_documents = serializers.FileField(required=False)

    @staticmethod
    def validate_role(value):
        try:
            return UserRole[value].value
        except KeyError:
            raise serializers.ValidationError("Некорректная роль пользователя")

    def validate(self, data):
        request = self.context.get("request")
        if data["role"] == "SELLER" or data["role"] == UserRole.SELLER.name:
            if not data.get("organization_name") or not request.FILES.get("organization_documents"):
                raise serializers.ValidationError("Продавец должен указать название "
                                                  "организацию и загрузить документы.")
        return data

    def create(self, validated_data):
        request = self.context.get("request")
        return self.register_user.execute(validated_data, request.FILES)