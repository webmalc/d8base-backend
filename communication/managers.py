"""The communication managers module."""
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from django.db import models
from django.db.models.query import QuerySet

from users.models import User

if TYPE_CHECKING:
    from professionals.models import Professional


class ReviewManager(models.Manager):
    """The review manager."""

    def get_list(self) -> QuerySet:
        """Return a list of reviews."""
        return self.all().select_related(
            'user',
            'professional',
            'created_by',
            'modified_by',
        )

    # TODO: Test it
    def get_professional_rating(self, professional: 'Professional') -> Decimal:
        """Get the average professional rating."""
        return self.filter(professional=professional).\
            aggregate(models.Avg('rating'))['rating__avg']


class MessagesManager(models.Manager):
    """The messages manager."""

    def get_list(self) -> QuerySet:
        """Return a list of messages."""
        return self.all().select_related(
            'sender',
            'recipient',
            'created_by',
            'modified_by',
        )

    def get_sent_messages(
        self,
        user: Optional[User] = None,
        is_read: Optional[bool] = None,
    ) -> QuerySet:
        """Return a list of user sent messages."""
        query = self.get_list().filter(is_deleted_from_sender=False)
        if user is not None:
            query = query.filter(recipient=user)
        if is_read is not None:
            query = query.filter(is_read=is_read)
        return query

    def get_received_messages(
        self,
        user: Optional[User] = None,
        is_read: Optional[bool] = None,
    ) -> QuerySet:
        """Return a list of user received messages."""
        query = self.get_list().filter(is_deleted_from_recipient=False)
        if user is not None:
            query = query.filter(recipient=user)
        if is_read is not None:
            query = query.filter(is_read=is_read)
        return query
