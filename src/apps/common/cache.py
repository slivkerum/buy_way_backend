from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Generic,
    TypeVar,
)

from django.core.cache import cache


TData = TypeVar("TData")


class BaseCacheClient(ABC, Generic[TData]):
    @abstractmethod
    def cache_data(self, data: TData, key: str, ttl: int):
        ...

    @abstractmethod
    def fetch_cached_data(self, key: str) -> TData:
        ...


class RedisCacheClient(BaseCacheClient):
    def cache_data(self, data: TData, key: str, ttl: int):
        cache.set(key, data, timeout=ttl)

    def fetch_cached_data(self, key: str) -> TData:
        return cache.get(key)
