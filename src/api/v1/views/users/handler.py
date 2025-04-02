import uuid

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from apps.users.entities.users import UserEntity
from api.v1.serializers.users import (
    CreateUserSerializer
)
from apps.users.services.users import BaseUserService
from config.containers import get_container


class CreateUserAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    @staticmethod
    def post(request) -> Response:
        container = get_container()
        user_service: BaseUserService = container.resolve(BaseUserService)
        create_user_serializer = CreateUserSerializer(data=request.data)

        if not create_user_serializer.is_valid():
            return Response(create_user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserEntity(
                id = uuid.uuid4(),
                email = create_user_serializer.validated_data['email'],
                password= create_user_serializer.validated_data['password'],
                first_name='',
                last_name='',
                role = create_user_serializer.validate_role(request.data['role']),
                is_active=True,
                enters_count=0
            )

            user_service.create_user(user)

            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteUserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def delete(request) -> Response:
        container = get_container()
        user_service: BaseUserService = container.resolve(BaseUserService)

        success = user_service.soft_delete_user(request.user.id)
        if not success:
            return Response({"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"detail": "Ваш аккаунт удален."}, status=status.HTTP_204_NO_CONTENT)