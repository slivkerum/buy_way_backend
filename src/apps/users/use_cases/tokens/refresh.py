from dataclasses import dataclass

from apps.users.entities.tokens import (
    TokenPairEntity,
    TokenType,
)
from apps.users.entities.users import UserEntity
from apps.users.services.tokens import (
    BaseTokenizerService,
    BaseTokenService,
    BaseTokenValidatorService,
)
from apps.users.services.users import BaseUserService


@dataclass
class RefreshTokenUseCase:
    user_service: BaseUserService
    tokenizer: BaseTokenizerService
    token_validator_service: BaseTokenValidatorService
    token_service: BaseTokenService

    def execute(self, refresh_token: str) -> tuple[TokenPairEntity, UserEntity]:
        decoded_refresh_token = self.tokenizer.decode_token(encoded_token=refresh_token)
        self.token_validator_service.validate(token=decoded_refresh_token, token_type=TokenType.REFRESH)

        user = self.user_service.get_user_by_id(user_id=decoded_refresh_token.subject_id)

        access_token = self.tokenizer.create_access_token(user)
        refresh_token = self.tokenizer.create_refresh_token(user)

        # revoke refresh token that has been used
        self.token_service.revoke_token(jti=decoded_refresh_token.jti)

        self.token_service.save_token(refresh_token=self.tokenizer.decode_token(encoded_token=refresh_token))
        return TokenPairEntity(access_token=access_token, refresh_token=refresh_token), user
