import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.users.entities.users import UserEntity
from apps.users.repositories.users import UserRepository
from apps.users.serializers.users import (
    UserCreateSerializer,
    UserResponseSerializer
)
from apps.users.services.users import UserService


class CreateUserAPIView(APIView):

    @staticmethod
    def post(request) -> Response:
        serializer = UserCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = UserEntity(
            id=uuid.uuid4(),
            email=serializer.validated_data['email'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],
            role=serializer.validated_data['role'],
            password=serializer.data['password'],
        )

        user_service = UserService(UserRepository())

        try:
            user_service.create_user(user)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response_serializer = UserResponseSerializer(user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)