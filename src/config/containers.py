from functools import lru_cache

import punq

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
from apps.users.repositories.users import (
    BaseUserRepository,
    UserRepository,
)
from apps.users.services.users import (
    BaseUserService,
    UserService,
)
from apps.users.use_cases.register_user import (
    RegisterUserUseCase,
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

    container.register(BaseUserService, UserService)
    container.register(BaseProductService, ProductService)
    container.register(BaseCategoryService, CategoryService)
    container.register(BaseCharacteristicService, CharacteristicService)

    container.register(RegisterUserUseCase)

    return container

