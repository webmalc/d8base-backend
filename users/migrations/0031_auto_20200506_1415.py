# Generated by Django 3.0.5 on 2020-05-06 14:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.CITIES_COUNTRY_MODEL),
        ('cities', '0011_auto_20180108_0706'),
        migrations.swappable_dependency(settings.CITIES_CITY_MODEL),
        ('users', '0030_auto_20200506_0830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlocation',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='userlocation_locations', to=settings.CITIES_CITY_MODEL, verbose_name='city'),
        ),
        migrations.AlterField(
            model_name='userlocation',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userlocation_locations', to=settings.CITIES_COUNTRY_MODEL, verbose_name='country'),
        ),
        migrations.AlterField(
            model_name='userlocation',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='userlocation_locations', to='cities.District', verbose_name='district'),
        ),
        migrations.AlterField(
            model_name='userlocation',
            name='postal_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='userlocation_locations', to='cities.PostalCode', verbose_name='postal code'),
        ),
        migrations.AlterField(
            model_name='userlocation',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='userlocation_locations', to='cities.Region', verbose_name='region'),
        ),
        migrations.AlterField(
            model_name='userlocation',
            name='subregion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='userlocation_locations', to='cities.Subregion', verbose_name='subregion'),
        ),
    ]
