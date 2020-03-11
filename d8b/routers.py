"""The d8b router module."""
from rest_framework.routers import DefaultRouter as BaseRouter

from location.routers import get_router as get_location_router


class DefaultRouter(BaseRouter):
    """The default router class."""

    def extend(self, *args):
        """Extend the default router with other routers."""
        for router in args:
            self.registry.extend(router.registry)


def get_router_urls() -> list:
    """Return the default router URLs."""
    router = DefaultRouter()
    router.extend(get_location_router())
    return router.urls