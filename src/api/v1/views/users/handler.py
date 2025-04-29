from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from apps.users.services.organizations import BaseOrganizationService
from apps.users.services.users import BaseUserService
from apps.users.exceptions.organizations import (
    InvalidAddFile
)

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


class OrganizationAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def post(request) -> Response:
        container = get_container()
        organization_service: BaseOrganizationService = container.resolve(BaseOrganizationService)
        user_service: BaseUserService = container.resolve(BaseUserService)

        user = user_service.get_user_by_email(request.user)
        try:
            organization = organization_service.get_user_organizations(user.id)

            organization_service.add_file(
                organization.id,
                request.FILES["organization_documents"]
            )

            return Response(
                {"detail": "Файл успешно добавлен"},
                status=status.HTTP_200_OK
            )
        except InvalidAddFile:
            return Response(
                InvalidAddFile().message,
                status=status.HTTP_400_BAD_REQUEST
            )


    @staticmethod
    def delete(request) -> Response:
        container = get_container()
        organization_service: BaseOrganizationService = container.resolve(BaseOrganizationService)
        user_service: BaseUserService = container.resolve(BaseUserService)

        file_id = request.data.get("file_id")
        user = user_service.get_user_by_email(request.user)

        try:
            organization = organization_service.get_user_organizations(user.id)

            organization_service.remove_file(organization.id, file_id)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Файл успешно удален"}, status=status.HTTP_200_OK)
