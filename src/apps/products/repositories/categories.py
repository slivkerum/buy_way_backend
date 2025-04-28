from abc import ABC, abstractmethod
from apps.products.models.categories import Category
from apps.products.entities.categories import CategoryEntity
from apps.products.exceptions.categories import CategoryNotFound


class BaseCategoryRepository(ABC):

    @abstractmethod
    def get_all(self) -> list[CategoryEntity]: ...

    @abstractmethod
    def get_by_id(self, category_id: int) -> CategoryEntity: ...


class CategoryRepository(BaseCategoryRepository):

    def get_all(self) -> list[CategoryEntity]:
        return [cat.to_entity() for cat in Category.objects.all()]

    def get_by_id(self, category_id: int) -> CategoryEntity:
        category = Category.objects.filter(id=category_id).first()
        if not category:
            raise CategoryNotFound(category_id)
        return category.to_entity()
