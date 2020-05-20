"""The services tests module."""
import pytest
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet

from communication.validators import (validate_message_parent,
                                      validate_message_recipient)
from users.models import User

pytestmark = pytest.mark.django_db


def test_validate_message_recipient(admin: User, messages: QuerySet):
    """Should mark the message read."""
    message = messages.filter(sender=admin).first()
    validate_message_recipient(message)
    message.recipient = admin
    with pytest.raises(ValidationError):
        validate_message_recipient(message)


def test_validate_parent(admin: User, messages: QuerySet):
    """Should validate the message parent message."""
    messages = messages.filter(sender=admin)
    message = messages[0]
    message.parent = messages[1]
    with pytest.raises(ValidationError):
        validate_message_parent(message)
    message.is_read = True
    with pytest.raises(ValidationError):
        validate_message_parent(message)
    message.parent = messages.filter(recipient=admin).first()
    validate_message_parent(message)