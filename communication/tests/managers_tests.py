"""The services tests module."""
import pytest
from django.db.models.query import QuerySet

from communication.models import Message
from conftest import OBJECTS_TO_CREATE
from users.models import User

pytestmark = pytest.mark.django_db


def test_get_sent_messages(admin: User, messages: QuerySet):
    """Should return sent messages."""
    manager = Message.objects
    query = manager.get_sent_messages(admin)
    num = OBJECTS_TO_CREATE
    message = query.first()
    message.is_deleted_from_sender = True
    message.save()

    query = manager.get_sent_messages(admin)
    assert num - 1 == query.count()
    assert num != messages.count()

    message = query.first()
    message.is_read = True
    message.save()
    assert num - 2 == manager.get_sent_messages(admin, is_read=False).count()


def test_get_received_messages(admin: User, messages: QuerySet):
    """Should return received messages."""
    manager = Message.objects
    query = manager.get_received_messages(admin)
    num = OBJECTS_TO_CREATE
    message = query.first()
    message.is_deleted_from_recipient = True
    message.save()

    query = manager.get_received_messages(admin)
    assert num - 1 == query.count()
    assert num != messages.count()

    message = query.first()
    message.is_read = True
    message.save()
    assert num - 2 == manager.get_received_messages(admin,
                                                    is_read=False).count()
