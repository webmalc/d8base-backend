# Generated by Django 3.0.7 on 2020-07-14 20:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('professionals', '0019_auto_20200713_1849'),
        ('services', '0008_auto_20200714_2000'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='servicelocation',
            unique_together={('location', 'service')},
        ),
    ]
