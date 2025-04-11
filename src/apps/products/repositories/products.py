from itertools import product
from uuid import UUID
from abc import ABC, abstractmethod

from apps.products.models.products import Product
from apps.products.entities.products import ProductEntity
from apps.products.exceptions.products import ProductNotFound


class BaseProductRepository(ABC):

    @abstractmethod
    def get_all(self) -> list[ProductEntity]:...

    @abstractmethod
    def get_product_by_id(self, product_id: UUID) -> ProductEntity: ...

    @abstractmethod
    def create_product(self, product: ProductEntity) -> ProductEntity: ...

    @abstractmethod
    def update_product(self, product: ProductEntity) -> ProductEntity: ...

    @abstractmethod
    def delete_product(self, product_id: UUID) -> None: ...


class ProductRepository(BaseProductRepository):

    def get_all(self) -> list[ProductEntity]:
        return [product.to_entity() for product in Product.objects.all()]

    def get_product_by_id(self, product_id: UUID) -> ProductEntity:
        product = Product.objects.filter(id=product_id).first()
        if not product:
            raise ProductNotFound(product_id)
        return product.to_entity()

    def create_product(self, product: ProductEntity) -> ProductEntity:
        new_product = Product.objects.create(
            id=product.id,
            title=product.title,
            amount=product.amount,
            description=product.description,
            category_id=product.category.id,
        )

        characteristic_ids = [option.id for option in product.product_characteristic]
        new_product.product_characteristics.set(characteristic_ids)

        return new_product.to_entity()

    def update_product(self, product: ProductEntity) -> ProductEntity:
        product_db = Product.objects.get(id=product.id)

        product_db.title = product.title
        product_db.amount = product.amount
        product_db.description = product.description
        product_db.category_id = product.category.id
        product_db.save()

        characteristic_ids = [option.id for option in product.product_characteristic]
        product_db.product_characteristics.set(characteristic_ids)

        return product_db.to_entity()

    def delete_product(self, product_id: UUID) -> None:
        Product.objects.filter(id=product_id).delete()
