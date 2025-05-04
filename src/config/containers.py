from functools import lru_cache

import punq

from apps.products.repositories.cart import (
    BaseCartRepository,
    CartRepository,
)
from apps.products.repositories.categories import (
    BaseCategoryRepository,
    CategoryRepository,
)
from apps.products.repositories.characteristics import (
    BaseCharacteristicRepository,
    CharacteristicRepository,
)
from apps.products.repositories.products import (
    BaseProductRepository,
    ProductRepository,
)
from apps.products.repositories.reviews import (
    BaseReviewRepository,
    ReviewRepository,
)
from apps.products.services.cart import (
    BaseCartService,
    CartService,
)
from apps.products.services.categories import (
    BaseCategoryService,
    CategoryService,
)
from apps.products.services.characteristics import (
    BaseCharacteristicService,
    CharacteristicService,
)
from apps.products.services.products import (
    BaseProductService,
    ProductService,
)
from apps.products.services.reviews import (
    BaseReviewService,
    ReviewService,
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
from apps.users.use_cases.users.register_user import (
    RegisterUserUseCase,
)
from apps.users.use_cases.users.create_cart import (
    CreateCartUseCases
)


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_container() -> punq.Container:
    container = punq.Container()

    container.register(BaseUserRepository, UserRepository)
    container.register(BaseProductRepository, ProductRepository)
    container.register(BaseCategoryRepository, CategoryRepository)
    container.register(BaseCharacteristicRepository, CharacteristicRepository)
    container.register(BaseReviewRepository, ReviewRepository)
    container.register(BaseOrganizationRepository, OrganizationRepository)
    container.register(BaseCartRepository, CartRepository)

    container.register(BaseUserService, UserService)
    container.register(BaseProductService, ProductService)
    container.register(BaseCategoryService, CategoryService)
    container.register(BaseCharacteristicService, CharacteristicService)
    container.register(BaseReviewService, ReviewService)
    container.register(BaseOrganizationService, OrganizationService)
    container.register(BaseCartService, CartService)

    container.register(CreateCartUseCases)
    container.register(RegisterUserUseCase)
    container.register(SendEmailConfirmationCodeUseCase)
    container.register(ConfirmEmailCodeUseCase)

    return container

