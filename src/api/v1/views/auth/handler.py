from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from api.v1.serializers.auth import RegisterSerializer
from api.v1.serializers.email_confirmation import ConfirmEmailSerializer

from config.containers import get_container

from apps.users.use_cases.users.email_confirmation.confirm import (
    ConfirmEmailCodeUseCase
)

class RegisterUserView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def get_serializer_context(self):
        return {"request": self.request}


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        container = get_container()
        use_cases: ConfirmEmailCodeUseCase = container.resolve(ConfirmEmailCodeUseCase)

        serializer = ConfirmEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]

        try:
            use_cases.execute(email, code)
            return Response({"detail": "Email подтвержден."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)