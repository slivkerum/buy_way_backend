from functools import lru_cache

import punq

from apps.common.cache import (
    BaseCacheClient,
    RedisCacheClient,
)
from apps.users.repositories.organizations import (
    BaseOrganizationRepository,
    OrganizationRepository,
)
from apps.users.repositories.users import (
    BaseUserRepository,
    UserRepository,
)
from apps.users.services.organizations import (
    BaseOrganizationService,
    OrganizationService,
)
from apps.users.services.users import (
    BaseUserService,
    UserService,
)
from apps.users.use_cases.users.email_confirmation.send import (
    SendEmailConfirmationCodeUseCase
)
from apps.users.use_cases.users.email_confirmation.confirm import (
    ConfirmEmailCodeUseCase
)
from apps.users.use_cases.users.email_confirmation.send import (
    SendEmailConfirmationCodeUseCase,
)
from apps.users.use_cases.users.create import (
    CreateUserUseCase
)
from apps.users.repositories.tokens import (
    BaseTokenRepository,
    TokenRepository,
)
from apps.users.services.tokens import (
    BaseTokenizerService,
    BaseTokenService,
    BaseTokenValidatorService,
    ComposedTokenValidatorService,
    TokenExpiryValidatorService,
    TokenizerService,
    TokenRevokedValidatorService,
    TokenService,
    TokenTypeValidatorService,
)
from apps.users.use_cases.auth.authenticate import AuthenticateUseCase
from apps.users.use_cases.tokens.get import GetTokenPairUseCase
from apps.users.use_cases.tokens.refresh import RefreshTokenUseCase
from apps.users.use_cases.tokens.revoke import RevokeTokenUseCase



@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_container() -> punq.Container:
    container = punq.Container()

    container.register(BaseUserRepository, UserRepository)
    container.register(BaseTokenRepository, TokenRepository)

    container.register(BaseUserService, UserService)
    container.register(BaseTokenService, TokenService)
    container.register(BaseTokenizerService, TokenizerService)

    container.register(TokenTypeValidatorService)
    container.register(TokenExpiryValidatorService)
    container.register(TokenRevokedValidatorService)

    def build_token_validators() -> BaseTokenValidatorService:
        return ComposedTokenValidatorService(
            validators=[
                container.resolve(TokenTypeValidatorService),
                container.resolve(TokenExpiryValidatorService),
                container.resolve(TokenRevokedValidatorService),
            ],
        )

    container.register(BaseTokenValidatorService, factory=build_token_validators)

    container.register(AuthenticateUseCase)
    container.register(GetTokenPairUseCase)
    container.register(RefreshTokenUseCase)
    container.register(RevokeTokenUseCase)

    container.register(SendEmailConfirmationCodeUseCase)
    container.register(ConfirmEmailCodeUseCase)
    container.register(CreateUserUseCase)

    container.register(BaseOrganizationRepository, OrganizationRepository)

    container.register(BaseUserService, UserService)
    container.register(BaseOrganizationService, OrganizationService)
    container.register(SendEmailConfirmationCodeUseCase)
    container.register(ConfirmEmailCodeUseCase)

    return container

