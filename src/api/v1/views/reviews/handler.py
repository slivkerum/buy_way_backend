from uuid import UUID
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from config.containers import get_container
from apps.products.services.reviews import BaseReviewService
from api.v1.serializers.reviews import ReviewSerializer


class ReviewListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, product_id: UUID):
        container = get_container()
        service: BaseReviewService = container.resolve(BaseReviewService)

        reviews = service.get_reviews_by_product(product_id)
        data = [ReviewSerializer.from_entity(r) for r in reviews]
        return Response(data)

    def post(self, request, product_id: UUID):
        serializer = ReviewSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        container = get_container()
        service: BaseReviewService = container.resolve(BaseReviewService)

        review_entity = serializer.to_entity(product_id, user_id=request.user.id)
        created = service.add_review(review_entity)
        return Response(ReviewSerializer.from_entity(created), status=status.HTTP_201_CREATED)


class ReviewDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, review_id: int):
        container = get_container()
        service: BaseReviewService = container.resolve(BaseReviewService)

        service.delete_review(review_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, review_id: int):
        container = get_container()
        service: BaseReviewService = container.resolve(BaseReviewService)

        try:
            review = service.get_review_by_id(review_id)
            data = ReviewSerializer.from_entity(review)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
