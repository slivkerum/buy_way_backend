from ninja import Router

from api.v1.users.handlers import router as users_router
from api.v1.organizations.handlers import router as organizations_router
from api.v1.products.handlers import router as products_router
from api.v1.characteristics.handlers import router as characteristics_router
from api.v1.categories.handlers import router as categories_router
from api.v1.cart.handlers import router as cart_router
from api.v1.reviews.handlers import router as reviews_router


router = Router(tags=["v1"])
router.add_router('users/', users_router)
router.add_router('organizations/', organizations_router)
router.add_router('products/', products_router)
router.add_router('characteristics/', characteristics_router)
router.add_router('categories/', categories_router)
router.add_router('cart/', cart_router)
router.add_router('reviews/', reviews_router)