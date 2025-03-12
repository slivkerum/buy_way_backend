from rest_framework import serializers
from apps.users.entities.users import UserRole

class UserCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    email = serializers.EmailField(required=True, max_length=255)
    password = serializers.CharField(required=True, write_only=True, max_length=255)
    role = serializers.ChoiceField(choices=[role.value for role in UserRole], required=False)

class UserResponseSerializer(serializers.Serializer):
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    role = serializers.CharField(read_only=True)