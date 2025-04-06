from uuid import UUID
from abc import ABC, abstractmethod

from apps.products.models.products import Product
from apps.products.entities.products import ProductEntity
from apps.products.exceptions.products import ProductNotFound


class BaseProductRepository(ABC):

    @abstractmethod
    def get_product_by_id(self, product_id: UUID) -> ProductEntity: ...

    @abstractmethod
    def create_product(self, product: ProductEntity) -> ProductEntity: ...

    @abstractmethod
    def update_product(self, product: ProductEntity) -> ProductEntity: ...

    @abstractmethod
    def delete_product(self, product_id: UUID) -> None: ...


class ProductRepository(BaseProductRepository):

    def get_product_by_id(self, product_id: UUID) -> ProductEntity:
        product = Product.objects.filter(id=product_id, is_deleted=False).first()
        if not product:
            raise ProductNotFound(product_id)
        return product.to_entity()

    def create_product(self, product: ProductEntity) -> ProductEntity:
        new_product = Product.objects.create(
            id=product.id,
            title=product.title,
            amount=product.amount,
            description=product.description,
            characteristic_id=product.product_characteristic.id
        )
        return new_product.to_entity()

    def update_product(self, product: ProductEntity) -> ProductEntity:
        Product.objects.filter(id=product.id).update(
            title=product.title,
            amount=product.amount,
            description=product.description,
            characteristic_id=product.product_characteristic.id
        )
        return self.get_product_by_id(product.id)

    def delete_product(self, product_id: UUID) -> None:
        Product.objects.filter(id=product_id).update(is_deleted=True)
