# Generated by Django 3.0.8 on 2020-08-24 18:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_profile_choose_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='About_you',
            field=models.CharField(default=django.utils.timezone.now, max_length=9),
            preserve_default=False,
        ),
    ]
