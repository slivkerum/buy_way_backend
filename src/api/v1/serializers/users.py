from rest_framework import serializers

from apps.users.entities.users import UserRole, UserEntity


class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        write_only=True,
        min_length=6
    )

    @staticmethod
    def validate_role(value):
        if value not in [role.value for role in UserRole]:
            raise serializers.ValidationError('Invalid role')
        return value


class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    role = serializers.ChoiceField(choices=[role.value for role in UserRole], required=False)

    @classmethod
    def from_entity(cls, user_entity: UserEntity) -> 'UserSerializer':
        return cls(
            id=user_entity.id,
            email=user_entity.email,
            first_name=user_entity.first_name,
            last_name=user_entity.last_name,
            role=user_entity.role,
        )