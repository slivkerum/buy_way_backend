from functools import lru_cache

import punq

from apps.users.repositories.users import (
    BaseUserRepository,
    UserRepository,
)
from apps.users.services.users import (
    BaseUserService,
    UserService,
)


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_container() -> punq.Container:
    container = punq.Container()

    container.register(BaseUserRepository, UserRepository)

    container.register(BaseUserService, UserService)

    return container

