import uuid
from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from datetime import (
    datetime,
    timedelta,
)

from django.conf import settings

from jose import (
    jwt,
    JWTError,
)

from apps.users.entities.tokens import (
    TokenEntity,
    TokenType,
)
from apps.users.entities.users import UserEntity
from apps.users.exceptions.tokens import (
    IncorrectTokenValueException,
    TokenExpiredException,
    TokenIncorrectTypeException,
    TokenRevokedException,
)
from apps.users.repositories.tokens import BaseTokenRepository


class BaseTokenService(ABC):

    @abstractmethod
    def save_token(self, refresh_token: TokenEntity) -> None: ...

    @abstractmethod
    def revoke_token(self, jti: str) -> None: ...

    @abstractmethod
    def check_revoked(self, jti: str) -> bool: ...


@dataclass
class TokenService(BaseTokenService):
    token_repository: BaseTokenRepository

    def save_token(self, refresh_token: TokenEntity) -> None:
        return self.token_repository.save_token(refresh_token=refresh_token)

    def revoke_token(self, jti: str) -> None:
        return self.token_repository.revoke_token(jti=jti)

    def check_revoked(self, jti: str) -> bool:
        return self.token_repository.check_revoked(jti=jti)


class BaseTokenizerService(ABC):

    @abstractmethod
    def create_access_token(self, user: UserEntity) -> str: ...

    @abstractmethod
    def create_refresh_token(self, user: UserEntity) -> str: ...

    @abstractmethod
    def decode_token(self, encoded_token: str) -> TokenEntity: ...


class TokenizerService(BaseTokenizerService):

    def create_access_token(self, user: UserEntity) -> str:
        expires_at = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return self._encode_token(token_type=TokenType.ACCESS, expires_at=expires_at, subject_id=user.id)

    def create_refresh_token(self, user: UserEntity) -> str:
        expires_at = datetime.now() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        return self._encode_token(token_type=TokenType.REFRESH, expires_at=expires_at, subject_id=user.id)

    def decode_token(self, encoded_token: str) -> TokenEntity:
        try:
            payload = jwt.decode(encoded_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        except JWTError:
            raise IncorrectTokenValueException(token=encoded_token)
        else:
            token = TokenEntity(
                subject_id=payload['subject_id'],
                token_type=payload['token_type'],
                jti=payload['jti'],
                expires_at=self._convert_from_unix_datetime(unix_datetime=payload['expires_at']),
            )
            return token

    def _encode_token(self, token_type: TokenType, expires_at: datetime, subject_id: str) -> str:
        jti = self._generate_jti()
        to_encode = {
            "expires_at": self._convert_to_unix_datetime(datetime_object=expires_at),
            "subject_id": str(subject_id),
            "jti": jti,
            "token_type": token_type,
        }
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def _generate_jti() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def _convert_to_unix_datetime(datetime_object: datetime) -> int:
        return int(datetime_object.timestamp())

    @staticmethod
    def _convert_from_unix_datetime(unix_datetime: int) -> datetime:
        return datetime.fromtimestamp(unix_datetime)


class BaseTokenValidatorService(ABC):
    def validate(self, token: TokenEntity, token_type: TokenType) -> None:
        ...


class TokenTypeValidatorService(BaseTokenValidatorService):
    def validate(self, token: TokenEntity, token_type: TokenType) -> None:
        if token.token_type != token_type:
            raise TokenIncorrectTypeException(needed_type=token_type)


class TokenExpiryValidatorService(BaseTokenValidatorService):
    def validate(self, token: TokenEntity, *args, **kwargs) -> None:
        if token.expires_at < datetime.now():
            raise TokenExpiredException()


@dataclass
class TokenRevokedValidatorService(BaseTokenValidatorService):
    token_service: BaseTokenService

    def validate(self, token: TokenEntity, *args, **kwargs) -> None:
        if token.token_type == TokenType.REFRESH and self.token_service.check_revoked(jti=token.jti):
            raise TokenRevokedException()


@dataclass
class ComposedTokenValidatorService(BaseTokenValidatorService):
    validators: list[BaseTokenValidatorService]

    def validate(self, token: TokenEntity, token_type: TokenType) -> None:
        for validator in self.validators:
            validator.validate(token=token, token_type=token_type)
