# Generated by Django 2.2.11 on 2020-03-19 15:11

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.CITIES_COUNTRY_MODEL),
        migrations.swappable_dependency(settings.CITIES_CITY_MODEL),
        ('cities', '0011_auto_20180108_0706'),
        ('users', '0005_auto_20200318_1300'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='address')),
                ('coordinates', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326, verbose_name='coordinates')),
                ('is_default', models.BooleanField(default=False, help_text='is default location?', verbose_name='is default')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_locations', to=settings.CITIES_CITY_MODEL, verbose_name='city')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_locations', to=settings.CITIES_COUNTRY_MODEL, verbose_name='country')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users_userlocation_created_by', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_locations', to='cities.District', verbose_name='district')),
                ('modified_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users_userlocation_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='modified by')),
                ('postal_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_locations', to='cities.PostalCode', verbose_name='postal code')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_locations', to='cities.Region', verbose_name='region')),
                ('subregion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_locations', to='cities.Subregion', verbose_name='subregion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
