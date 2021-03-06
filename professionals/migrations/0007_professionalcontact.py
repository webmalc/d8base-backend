# Generated by Django 3.0.5 on 2020-05-06 09:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contacts', '0003_auto_20200406_1125'),
        ('professionals', '0006_auto_20200420_0955'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfessionalContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('value', models.CharField(max_length=255, verbose_name='value')),
                ('use_value_from_user', models.BooleanField(default=False, help_text='use value from the user?', verbose_name='value from user')),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='professionals_professionalcontact_contacts', to='contacts.Contact', verbose_name='contact')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='professionals_professionalcontact_created_by', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('modified_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='professionals_professionalcontact_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='modified by')),
                ('professional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='professionals.Professional', verbose_name='professional')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
                'unique_together': {('value', 'professional', 'contact')},
            },
        ),
    ]
