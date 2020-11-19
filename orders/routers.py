"""The orders routers module."""
from rest_framework.routers import SimpleRouter

from .views import ReceivedOrdersViewSet, SentOrdersViewSet


def get_router() -> SimpleRouter:
    """Return the app router."""
    router = SimpleRouter()
    router.register(
        r"accounts/orders/sent",
        SentOrdersViewSet,
        "user-orders-sent",
    )
    router.register(
        r"accounts/orders/received",
        ReceivedOrdersViewSet,
        "user-orders-received",
    )
    return router
