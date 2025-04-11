from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from apps.users.services.users import BaseUserService
from config.containers import get_container


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