from dataclasses import dataclass

from apps.users.entities.tokens import TokenType
from apps.users.entities.users import UserEntity
from apps.users.exceptions.users import UserNotActiveException
from apps.users.services.tokens import (
    BaseTokenizerService,
    BaseTokenValidatorService,
)
from apps.users.services.users import BaseUserService


@dataclass
class AuthenticateUseCase:
    user_service: BaseUserService
    tokenizer: BaseTokenizerService
    token_validator_service: BaseTokenValidatorService

    def execute(self, access_token: str) -> UserEntity:
        token = self.tokenizer.decode_token(encoded_token=access_token)
        self.token_validator_service.validate(token=token, token_type=TokenType.ACCESS)
        user = self.user_service.get_user_by_id(user_id=token.subject_id)

        if not user.is_active:
            raise UserNotActiveException

        return user
