from dataclasses import dataclass

from apps.users.entities.tokens import TokenType
from apps.users.services.tokens import (
    BaseTokenizerService,
    BaseTokenService,
    BaseTokenValidatorService,
)


@dataclass
class RevokeTokenUseCase:
    token_service: BaseTokenService
    tokenizer: BaseTokenizerService
    token_validator_service: BaseTokenValidatorService

    def execute(self, refresh_token: str) -> None:
        token = self.tokenizer.decode_token(encoded_token=refresh_token)
        self.token_validator_service.validate(token=token, token_type=TokenType.REFRESH)
        self.token_service.revoke_token(jti=token.jti)
