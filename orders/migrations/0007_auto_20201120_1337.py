# Generated by Django 3.0.10 on 2020-11-20 13:37

import communication.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20201120_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderreminder',
            name='is_reminded',
            field=models.BooleanField(db_index=True, default=False, editable=False, verbose_name='is reminded?'),
        ),
        migrations.AlterField(
            model_name='orderreminder',
            name='remind_before',
            field=models.PositiveIntegerField(db_index=True, help_text='number of minutes for a reminder before the event', validators=[communication.validators.validate_reminder_remind_before], verbose_name='remind'),
        ),
    ]
