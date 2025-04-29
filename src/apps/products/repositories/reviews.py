from abc import (
    ABC,
    abstractmethod
)
from uuid import UUID

from apps.products.models.reviews import Review
from apps.products.entities.reviews import ReviewEntity
from apps.products.exceptions.reviews import ReviewNotFound
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseReviewRepository(ABC):

    @abstractmethod
    def get_reviews_by_product(self, product_id: UUID) -> list[ReviewEntity]: ...

    @abstractmethod
    def create_review(self, review: ReviewEntity) -> ReviewEntity: ...

    @abstractmethod
    def delete_review(self, review_id: int) -> None: ...

    @abstractmethod
    def get_by_id(self, review_id: int) -> ReviewEntity: ...


class ReviewRepository(BaseReviewRepository):

    def get_reviews_by_product(self, product_id: UUID) -> list[ReviewEntity]:
        reviews = Review.objects.filter(product_id=product_id)
        return [review.to_entity() for review in reviews]

    def create_review(self, review: ReviewEntity) -> ReviewEntity:
        user = User.objects.get(id=review.user_id)

        new_review = Review.objects.create(
            user=user,
            product_id=review.product_id,
            rating=review.rating,
            text=review.text,
        )
        return new_review.to_entity()

    def delete_review(self, review_id: int) -> None:
        deleted, _ = Review.objects.filter(id=review_id).delete()
        if deleted == 0:
            raise ReviewNotFound(review_id)

    def get_by_id(self, review_id: int) -> ReviewEntity:
        review = Review.objects.filter(id=review_id).first()
        if not review:
            raise ReviewNotFound(review_id)
        return review.to_entity()
