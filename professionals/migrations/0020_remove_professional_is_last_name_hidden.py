# Generated by Django 3.0.9 on 2020-08-27 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('professionals', '0019_auto_20200713_1849'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='professional',
            name='is_last_name_hidden',
        ),
    ]
