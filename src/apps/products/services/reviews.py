from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from apps.products.entities.reviews import ReviewEntity
from apps.products.repositories.reviews import BaseReviewRepository


class BaseReviewService(ABC):

    @abstractmethod
    def get_reviews_by_product(self, product_id: UUID) -> list[ReviewEntity]: ...

    @abstractmethod
    def get_review_by_id(self, review_id: int) -> ReviewEntity: ...

    @abstractmethod
    def add_review(self, review: ReviewEntity) -> ReviewEntity: ...

    @abstractmethod
    def delete_review(self, review_id: int) -> None: ...


@dataclass
class ReviewService(BaseReviewService):
    repo: BaseReviewRepository

    def get_reviews_by_product(self, product_id: UUID) -> list[ReviewEntity]:
        return self.repo.get_reviews_by_product(product_id)

    def get_review_by_id(self, review_id: int) -> ReviewEntity:
        return self.repo.get_by_id(review_id)

    def add_review(self, review: ReviewEntity) -> ReviewEntity:
        return self.repo.create_review(review)

    def delete_review(self, review_id: int) -> None:
        self.repo.delete_review(review_id)
