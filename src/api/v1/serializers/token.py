from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.first_name + " " + user.last_name
        token['role'] = user.role

        return token



