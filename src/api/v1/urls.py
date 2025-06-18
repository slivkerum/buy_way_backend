from ninja import Router

from api.v1.users.handlers import router as users_router
from api.v1.organizations.handlers import router as organizations_router


router = Router(tags=["v1"])
router.add_router('users/', users_router)
router.add_router('organizations/', organizations_router)