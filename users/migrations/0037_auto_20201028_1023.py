# Generated by Django 3.0.10 on 2020-10-28 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0036_auto_20200710_1652'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='usercontact',
            index=models.Index(fields=['-modified', '-created'], name='users_userc_modifie_7a25b2_idx'),
        ),
        migrations.AddIndex(
            model_name='userlocation',
            index=models.Index(fields=['-modified', '-created'], name='users_userl_modifie_8ff69e_idx'),
        ),
        migrations.AddIndex(
            model_name='usersavedprofessional',
            index=models.Index(fields=['-modified', '-created'], name='users_users_modifie_40feeb_idx'),
        ),
        migrations.AddIndex(
            model_name='usersettings',
            index=models.Index(fields=['-modified', '-created'], name='users_users_modifie_92bde5_idx'),
        ),
    ]
