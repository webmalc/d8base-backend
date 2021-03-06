"""The services fixtures module."""

from decimal import Decimal

import pytest
from django.db.models.query import QuerySet
from djmoney.contrib.exchange.models import ExchangeBackend, Rate
from moneyed import EUR, USD, Money

from services.models import Price, Service

# pylint: disable=redefined-outer-name


@pytest.fixture
def rates() -> QuerySet:
    """Return a rates queryset."""
    backend = ExchangeBackend.objects.create(name="test", base_currency="USD")
    Rate.objects.create(currency="USD", value="10.5", backend=backend)
    Rate.objects.create(currency="EUR", value="1.5", backend=backend)
    Rate.objects.create(currency="CAD", value="0.5", backend=backend)

    return Rate.objects.all()


@pytest.fixture
def services(
    professionals: QuerySet,
    professional_locations: QuerySet,
) -> QuerySet:
    """Return a services queryset."""
    for professional in professionals:
        first = Service.objects.create(
            professional=professional,
            name=f"1 for professional #{professional.pk}",
            description=f"1 description for professional #{professional.pk}",
            duration=60,
            service_type=Service.TYPE_ONLINE,
            is_enabled=True,
        )
        first.price = Price.objects.create(
            service=first,
            price=Money(10, EUR),
            payment_methods=["cash"],
        )
        first.tags.create(name="one")
        first.tags.create(name="two")
        first.tags.create(name="three")
        first.photos.create(
            name=f"name_{first.pk}",
            description=f"description_{first.pk}",
        )

        second = Service.objects.create(
            professional=professional,
            name=f"2 for professional #{professional.pk}",
            description=f"2 description for professional #{professional.pk}",
            duration=45,
            service_type=Service.TYPE_CLIENT_LOCATION,
            is_enabled=False,
            is_base_schedule=False,
        )
        second.price = Price.objects.create(
            service=second,
            is_price_fixed=False,
            start_price=Money(10, USD),
            end_price=Money(22.5, USD),
            payment_methods=["cash", "online"],
        )
        second.tags.create(name="one")
        second.tags.create(name="two")
        second.locations.create(
            max_distance=Decimal("20.0"),
            location=professional_locations.filter(
                professional=professional).first(),
        )
        second.photos.create(
            name=f"name_{second.pk}",
            description=f"description_{second.pk}",
        )
    return Service.objects.get_list()
