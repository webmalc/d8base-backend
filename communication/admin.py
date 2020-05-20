"""The communication admin module."""
from typing import Tuple, Type

from django.contrib import admin
from push_notifications.admin import GCMDeviceAdmin as BaseGCMDeviceAdmin
from push_notifications.models import GCMDevice
from reversion.admin import VersionAdmin

from users.admin_fiters import UserFilter

from .admin_fiters import RecipientFilter, SenderFilter
from .models import Message

admin.site.unregister(GCMDevice)


@admin.register(GCMDevice)
class GCMDeviceAdmin(VersionAdmin, BaseGCMDeviceAdmin):
    """The groups admin class."""

    list_filter = (UserFilter, 'active', 'cloud_message_type')
    autocomplete_fields = ('user', )

    class Media:
        """Required for the AutocompleteFilter."""


@admin.register(Message)
class MessageAdmin(VersionAdmin):
    """The messages admin class."""

    model: Type = Message
    list_display = ('id', 'sender', 'recipient', 'subject', 'is_read',
                    'read_datetime', 'created', 'created_by')
    list_display_links = ('id', 'sender', 'subject')
    list_filter = (SenderFilter, RecipientFilter, 'is_read', 'created')
    search_fields = ('=id', 'sender__last_name', 'recipient__last_name',
                     'subject', 'body')
    readonly_fields = (
        'created',
        'modified',
        'created_by',
        'modified_by',
        'is_read',
        'read_datetime',
        'is_deleted_from_recipient',
        'is_deleted_from_sender',
        'delete_from_recipient_datetime',
        'delete_from_sender_datetime',
    )

    autocomplete_fields = ('sender', 'recipient', 'parent')
    fieldsets: Tuple = (
        ('General', {
            'fields': ('sender', 'recipient')
        }),
        ('Message', {
            'fields': ('parent', 'subject', 'body')
        }),
        ('Options', {
            'fields':
                ('is_read', 'read_datetime', 'is_deleted_from_sender',
                 'delete_from_sender_datetime', 'is_deleted_from_recipient',
                 'delete_from_recipient_datetime', 'created', 'modified',
                 'created_by', 'modified_by')
        }),
    )
    list_select_related = ('sender', 'recipient', 'created_by')

    class Media:
        """Required for the AutocompleteFilter."""