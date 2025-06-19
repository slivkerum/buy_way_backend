from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from uuid import UUID

from apps.products.repositories.products import BaseProductRepository
from apps.products.entities.products import ProductEntity



class BaseProductService(ABC):

    @abstractmethod
    def get_all(self) -> list[ProductEntity]:
        ...

    @abstractmethod
    def get_product(self, product_id: UUID) -> ProductEntity:
        ...

    @abstractmethod
    def create_product(self, product: ProductEntity) -> ProductEntity:
        ...

    @abstractmethod
    def update_product(self, product: ProductEntity) -> ProductEntity:
        ...

    @abstractmethod
    def delete_product(self, product: UUID) -> ProductEntity:
        ...

@dataclass()
class ProductService(BaseProductService):
    repo: BaseProductRepository

    def get_all(self) -> list[ProductEntity]:
        return self.repo.get_all()

    def get_product(self, product_id: UUID) -> ProductEntity:
        return self.repo.get_product_by_id(product_id)

    def create_product(self, product: ProductEntity) -> ProductEntity:
        return self.repo.create_product(product)

    def update_product(self, product: ProductEntity) -> ProductEntity:
        return self.repo.update_product(product)

    def delete_product(self, product_id: UUID):
        self.repo.delete_product(product_id)
