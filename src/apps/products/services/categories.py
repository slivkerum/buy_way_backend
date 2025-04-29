from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from apps.products.repositories.categories import BaseCategoryRepository
from apps.products.entities.categories import CategoryEntity


class BaseCategoryService(ABC):

    @abstractmethod
    def get_all_categories(self) -> list[CategoryEntity]:
        ...

    @abstractmethod
    def get_category_by_id(self, category_id: int) -> CategoryEntity:
        ...


@dataclass
class CategoryService(BaseCategoryService):
    repo: BaseCategoryRepository

    def get_all_categories(self) -> list[CategoryEntity]:
        return self.repo.get_all()

    def get_category_by_id(self, category_id: int) -> CategoryEntity:
        return self.repo.get_by_id(category_id)
