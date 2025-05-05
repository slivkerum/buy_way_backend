from uuid import UUID
from dataclasses import dataclass

from apps.products.services.cart import (
    BaseCartService,
)


@dataclass
class CreateCartUseCases:
    cart_service: BaseCartService

    def create(self, user_id: UUID):
        self.cart_service.create_cart(user_id)

