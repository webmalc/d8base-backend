# Generated by Django 3.0.5 on 2020-04-30 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0027_auto_20200430_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='account_type',
            field=models.CharField(choices=[('user', 'user'), ('professional', 'professional')], default='user', max_length=20, verbose_name='account type'),
        ),
    ]
