"""The orders models module."""
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Type

import arrow
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MinMoneyValidator
from phonenumber_field.modelfields import PhoneNumberField

from communication.models import AbstractReminder
from d8b.models import CommonInfo, ValidationMixin
from orders import validators as orders_validators
from schedule.models import AbstractPeriod

from .managers import OrderRemindersManager, OrdersManager
from .services import (OrderAutoFiller, copy_contacts_from_order_to_user,
                       notify_order_update)

if TYPE_CHECKING:
    from users.models import User, UserLocation
    from services.models import Service, ServiceLocation


class Order(AbstractPeriod, CommonInfo, ValidationMixin):
    """The order class."""

    filler: Type = OrderAutoFiller
    copy_contacts: Callable[["Order"], None] = copy_contacts_from_order_to_user
    notifier: Callable[["Order", bool], None] = notify_order_update

    validators: List[Callable[["Order"], None]] = [
        orders_validators.validate_order_dates,
        orders_validators.validate_order_status,
        orders_validators.validate_order_client,
        orders_validators.validate_order_client_location,
        orders_validators.validate_order_service_location,
        orders_validators.validate_order_availability,
    ]

    objects: OrdersManager = OrdersManager()

    STATUS_NOT_CONFIRMED: str = "not_confirmed"
    STATUS_CONFIRMED: str = "confirmed"
    STATUS_PAID: str = "paid"
    STATUS_COMPLETED: str = "completed"
    STATUS_CANCELED: str = "canceled"
    STATUS_CHOICES = [
        (STATUS_NOT_CONFIRMED, _("not confirmed")),
        (STATUS_CONFIRMED, _("confirmed")),
        (STATUS_PAID, _("paid")),
        (STATUS_COMPLETED, _("completed")),
        (STATUS_CANCELED, _("canceled")),
    ]

    service: "Service" = models.ForeignKey(
        "services.Service",
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name=_("service"),
    )
    service_location: "ServiceLocation" = models.ForeignKey(
        "services.ServiceLocation",
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name=_("service location"),
        null=True,
        blank=True,
    )
    client_location: "UserLocation" = models.ForeignKey(
        "users.UserLocation",
        on_delete=models.SET_NULL,
        related_name="orders",
        verbose_name=_("client location"),
        null=True,
        blank=True,
    )
    client: "User" = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name=_("user"),
    )
    status = models.CharField(
        _("status"),
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NOT_CONFIRMED,
    )
    note = models.CharField(
        _("note"),
        null=True,
        blank=True,
        max_length=255,
    )
    price = MoneyField(
        max_digits=settings.D8B_MONEY_MAX_DIGITS,
        decimal_places=settings.D8B_MONEY_DECIMAL_PLACES,
        verbose_name=_("price"),
        null=True,
        blank=True,
        validators=[MinMoneyValidator(0)],
        db_index=True,
    )
    is_another_person = models.BooleanField(
        default=False,
        verbose_name=_("Order for another person?"),
        db_index=True,
    )
    first_name = models.CharField(
        _("first name"),
        max_length=30,
        null=False,
        blank=True,
    )
    last_name = models.CharField(
        _("last name"),
        max_length=150,
        null=False,
        blank=True,
    )
    phone = PhoneNumberField(
        _("phone"),
        blank=True,
        null=True,
        db_index=True,
    )

    def full_clean(self, exclude=None, validate_unique=True):
        """Validate the object."""
        self.filler(self).fill()
        return super().full_clean(exclude, validate_unique)

    def clean(self):
        """Validate the object."""
        self.filler(self).fill()
        return super().clean()

    def save(self, **kwargs):
        """Save the object."""
        is_created = not bool(self.pk)
        self.filler(self).fill()
        super().save(**kwargs)
        self.copy_contacts()
        self.notifier(is_created)

    @property
    def duration(self) -> float:
        """Return the order duration."""
        delta = self.end_datetime - self.start_datetime
        return delta.total_seconds() / 60

    def __str__(self) -> str:
        """Return the string representation."""
        return f"#{self.pk}: {super().__str__()}"

    class Meta(CommonInfo.Meta):
        """The metainformation."""

        abstract = False


class OrderReminder(AbstractReminder):
    """The order reminder."""

    subject: str = _("An order reminder.")
    template: str = "order_reminder"

    objects: OrderRemindersManager = OrderRemindersManager()

    validators: List[Callable[["OrderReminder"], None]] = [
        orders_validators.validate_order_reminder_recipient,
        orders_validators.validate_order_reminder_order
    ]

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="reminders",
        verbose_name=_("order"),
    )

    def get_data(self) -> Dict[str, Any]:
        """Return the data."""
        order: Order = self.order
        return {
            "id": order.pk,
            "note": order.note,
            "price": str(order.price),
            "first_name": order.first_name,
            "last_name": order.last_name,
            "phone": str(order.phone),
            "service": order.service.name,
        }

    def __str__(self) -> str:
        """Return the string representation."""
        return f"Order {super().__str__()}"

    def set_remind_before_datetime(self):
        """Set the remind_before_datetime field."""
        self.remind_before_datetime = arrow.get(self.order.start_datetime).\
            shift(minutes=-self.remind_before).datetime
