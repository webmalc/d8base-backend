# Generated by Django 3.0.5 on 2020-05-16 17:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('subject', models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='subject')),
                ('body', models.TextField(verbose_name='body')),
                ('is_read', models.BooleanField(db_index=True, default=False, editable=False, help_text='Has the message been read?', verbose_name='is read?')),
                ('read_datetime', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='read date')),
                ('is_deleted_from_sender', models.BooleanField(db_index=True, default=False, editable=False, help_text='Has the message been deleted from sender?', verbose_name='is deleted from sender?')),
                ('delete_from_sender_datetime', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='delete from sender datetime ')),
                ('is_deleted_from_recipient', models.BooleanField(db_index=True, default=False, editable=False, help_text='Has the message been deleted from recipient?', verbose_name='is deleted from recipient?')),
                ('delete_from_recipient_datetime', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='delete from recipient datetime ')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='communication_message_created_by', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('modified_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='communication_message_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='modified by')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='communication.Message')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to=settings.AUTH_USER_MODEL, verbose_name='recipient')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL, verbose_name='sender')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
