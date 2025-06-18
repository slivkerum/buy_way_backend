from dataclasses import dataclass

from apps.users.entities.tokens import TokenPairEntity
from apps.users.entities.users import UserEntity
from apps.users.exceptions.users import UserInvalidCredentialsException
from apps.users.services.tokens import (
    BaseTokenizerService,
    BaseTokenService,
)
from apps.users.services.users import BaseUserService


@dataclass
class GetTokenPairUseCase:
    user_service: BaseUserService
    tokenizer: BaseTokenizerService
    token_service: BaseTokenService

    def execute(self, email: str, password: str) -> tuple[TokenPairEntity, UserEntity]:
        user = self.user_service.get_user_by_email(email=email)

        is_equal = self.user_service.compare_passwords(given_password=password, user_password=user.password)
        if not is_equal:
            raise UserInvalidCredentialsException()

        access_token = self.tokenizer.create_access_token(user)
        refresh_token = self.tokenizer.create_refresh_token(user)

        self.token_service.save_token(refresh_token=self.tokenizer.decode_token(encoded_token=refresh_token))

        user.enters_count += 1
        self.user_service.update_user(user)

        return TokenPairEntity(access_token=access_token, refresh_token=refresh_token), user
