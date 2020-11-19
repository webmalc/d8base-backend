"""The views tests module."""
import arrow
import pytest
from django.db.models.query import QuerySet
from django.test.client import Client
from django.urls import reverse

from orders.models import Order
from users.models import User

pytestmark = pytest.mark.django_db


def test_user_received_order_list(
    user: User,
    client_with_token: Client,
    orders: QuerySet,
):
    """Should return a sent orders list."""
    query = orders.filter(service__professional__user=user)
    obj = query.first()
    response = client_with_token.get(reverse("user-orders-received-list"))
    data = response.json()
    assert response.status_code == 200
    assert data["count"] == query.count()
    assert data["results"][0]["service"] == obj.service.pk
    assert data["results"][0]["note"] == obj.note
    assert data["results"][0]["client"]["first_name"] == obj.client.first_name


def test_user_received_order_detail(
    user: User,
    client_with_token: Client,
    orders: QuerySet,
    user_locations: QuerySet,
):
    """Should return a received order."""
    query = orders.filter(service__professional__user=user)
    obj: Order = query.first()
    obj.client_location = user_locations.filter(user=user).first()
    obj.save()
    response = client_with_token.get(
        reverse("user-orders-received-detail", args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data["service"] == obj.service.pk
    assert data["note"] == obj.note
    assert data["client"]["last_name"] == obj.client.last_name
    assert data["client"]["gender"] == obj.client.gender
    assert data["price"] == str(obj.price.amount)
    assert data["price_currency"] == str(obj.price.currency)
    assert data["client_location"]["country"] == obj.client_location.country.pk


def test_user_received_order_display_restricted_entry(
    user: User,
    client_with_token: Client,
    orders: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = orders.exclude(service__professional__user=user).first()
    response = client_with_token.get(
        reverse("user-orders-received-detail", args=[obj.pk]))
    assert response.status_code == 404


def test_user_received_order_update(
    user: User,
    client_with_token: Client,
    orders: QuerySet,
    availability_slots: QuerySet,
):
    """Should be able to update a received order."""
    order: Order = orders.filter(service__professional__user=user).first()
    price = order.price
    slot = availability_slots.filter(service=order.service).last()
    response = client_with_token.patch(
        reverse("user-orders-received-detail", args=[order.pk]),
        {
            "note": "new note",
            "start_datetime": slot.start_datetime.isoformat(),
            "end_datetime": "",
            "price": "",
            "phone": "+12136210002",
        },
    )
    order.refresh_from_db()
    assert response.status_code == 200
    assert order.price != price
    assert order.price is not None
    assert order.modified_by == user
    assert order.end_datetime == arrow.get(
        order.start_datetime).shift(minutes=order.service.duration).datetime


def test_user_received_order_update_restricted_entry(
    user: User,
    client_with_token: Client,
    orders: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj: Order = orders.exclude(service__professional__user=user).first()
    response = client_with_token.post(
        reverse("user-orders-received-detail", args=[obj.pk]), {"note": "new"})
    assert response.status_code == 405


def test_user_send_orders_list(
    user: User,
    client_with_token: Client,
    orders: QuerySet,
):
    """Should return a sent orders list."""
    query = orders.exclude(service__professional__user=user)
    query.update(client=user)
    obj = query.first()
    response = client_with_token.get(reverse("user-orders-sent-list"))
    data = response.json()
    assert response.status_code == 200
    assert data["count"] == query.count()
    assert data["results"][0]["service"] == obj.service.pk
    assert data["results"][0]["note"] == obj.note


def test_user_sent_order_detail(
    user: User,
    client_with_token: Client,
    orders: QuerySet,
):
    """Should return a sent order."""
    query = orders.exclude(service__professional__user=user)
    query.update(client=user)
    obj = query.first()
    response = client_with_token.get(
        reverse("user-orders-sent-detail", args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data["price_amount"] == str(obj.price.amount)
    assert data["price_currency"] == str(obj.price.currency)


def test_user_sent_order_display_restricted_entry(
    client_with_token: Client,
    orders: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = orders.first()
    response = client_with_token.get(
        reverse("user-orders-sent-detail", args=[obj.pk]))
    assert response.status_code == 404


def test_user_sent_order_create(
    user: User,
    client_with_token: Client,
    services: QuerySet,
    availability_slots: QuerySet,
):
    """Should be able to create a sent order object."""
    service = services.exclude(professional__user=user).first()
    service.service_type = service.TYPE_PROFESSIONAL_LOCATION
    service.is_enabled = True
    service.save()
    slot = availability_slots.filter(service=service).last()
    response = client_with_token.post(
        reverse("user-orders-sent-list"),
        {
            "service": service.pk,
            "service_location": service.locations.first().pk,
            "start_datetime": slot.start_datetime.isoformat(),
            "note": "new sent order",
            "first_name": "new first name",
            "last_name": "new last name",
            "phone": "+12136210002",
        },
    )
    order = service.orders.first()
    assert response.status_code == 201
    assert order.note == "new sent order"
    assert order.end_datetime == arrow.get(
        order.start_datetime).shift(minutes=service.duration).datetime


def test_user_sent_order_update(
    user: User,
    client_with_token: Client,
    orders: QuerySet,
    availability_slots: QuerySet,
):
    """Should be able to update a sent order."""
    query = orders.exclude(service__professional__user=user)
    query.update(client=user)
    order = query.first()
    price = order.price
    slot = availability_slots.filter(service=order.service).last()
    response = client_with_token.patch(
        reverse("user-orders-sent-detail", args=[order.pk]),
        {
            "note": "new note",
            "start_datetime": slot.start_datetime.isoformat(),
            "end_datetime": "",
            "phone": "+12136210002",
        },
    )
    order.refresh_from_db()
    assert response.status_code == 200
    assert order.client == user
    assert order.price != price
    assert order.modified_by == user
    assert order.end_datetime == arrow.get(
        order.start_datetime).shift(minutes=order.service.duration).datetime


def test_user_sent_started_order_update(
    user: User,
    client_with_token: Client,
    orders: QuerySet,
):
    """Should deny access to someone else"s record."""
    query = orders.exclude(service__professional__user=user)
    query.update(client=user)
    order = query.first()
    order.start_datetime = arrow.utcnow().shift(hours=-1).datetime
    order.end_datetime = None
    order.save()
    response = client_with_token.patch(
        reverse("user-orders-sent-detail", args=[order.pk]),
        {
            "note": "new note",
            "phone": "+12136210002",
        },
    )
    assert response.status_code == 400
    assert response.json()["error"] == "Updating a started order is forbiden."


def test_user_sent_order_update_restricted_entry(
    client_with_token: Client,
    orders: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = orders.first()
    response = client_with_token.post(
        reverse("user-orders-sent-detail", args=[obj.pk]), {"note": "new"})
    assert response.status_code == 405
