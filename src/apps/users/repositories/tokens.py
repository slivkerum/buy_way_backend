from abc import (
    ABC,
    abstractmethod,
)

from apps.users.entities.tokens import TokenEntity
from apps.users.models.tokens import IssuedToken


class BaseTokenRepository(ABC):
    @abstractmethod
    def save_token(self, refresh_token: TokenEntity) -> None: ...

    @abstractmethod
    def revoke_token(self, jti: str) -> None: ...

    @abstractmethod
    def check_revoked(self, jti: str) -> bool: ...


class TokenRepository(BaseTokenRepository):

    def save_token(self, refresh_token: TokenEntity) -> None:
        token_dto = IssuedToken.from_entity(refresh_token=refresh_token)
        token_dto.save()

    def revoke_token(self, jti: str) -> None:
        IssuedToken.objects.filter(jti=jti).update(is_revoked=True)

    def check_revoked(self, jti: str) -> bool:
        return IssuedToken.objects.filter(jti=jti, is_revoked=True).exists()
