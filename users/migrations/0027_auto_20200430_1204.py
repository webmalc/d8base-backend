# Generated by Django 2.2.11 on 2020-04-30 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0026_auto_20200430_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersavedprofessional',
            name='note',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='note'),
        ),
    ]
