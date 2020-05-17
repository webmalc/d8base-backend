"""The communication models module."""
from django.db import models
from django.utils.translation import gettext_lazy as _

from d8b.models import CommonInfo, ValidationMixin
from users.models import User

from .managers import MessagesManager
from .validators import validate_message_parent, validate_message_recipient


class Message(CommonInfo, ValidationMixin):
    """The message class."""

    # notifications about new message

    validators = [validate_message_recipient, validate_message_parent]
    objects = MessagesManager()

    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name=_('sender'),
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages',
        verbose_name=_('recipient'),
    )
    subject = models.CharField(
        _('subject'),
        max_length=255,
        blank=True,
        null=True,
        db_index=True,
    )
    body = models.TextField(_('body'))
    is_read = models.BooleanField(
        default=False,
        editable=False,
        help_text=_('Has the message been read?'),
        verbose_name=_('is read?'),
        db_index=True,
    )
    read_datetime = models.DateTimeField(
        _('read date'),
        blank=True,
        null=True,
        editable=False,
    )
    is_deleted_from_sender = models.BooleanField(
        default=False,
        editable=False,
        help_text=_('Has the message been deleted from sender?'),
        verbose_name=_('is deleted from sender?'),
        db_index=True,
    )
    delete_from_sender_datetime = models.DateTimeField(
        _('delete from sender datetime '),
        blank=True,
        null=True,
        editable=False,
    )
    is_deleted_from_recipient = models.BooleanField(
        default=False,
        editable=False,
        help_text=_('Has the message been deleted from recipient?'),
        verbose_name=_('is deleted from recipient?'),
        db_index=True,
    )
    delete_from_recipient_datetime = models.DateTimeField(
        _('delete from recipient datetime '),
        blank=True,
        null=True,
        editable=False,
    )

    def __str__(self) -> str:
        """Return the string representation."""
        return f'{self.sender}->{self.recipient}: {self.subject}'

    class Meta(CommonInfo.Meta):
        """The metainformation."""

        abstract = False
