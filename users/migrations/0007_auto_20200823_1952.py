# Generated by Django 3.0.8 on 2020-08-23 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20200823_1630'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='bio',
            new_name='Write_your_bio',
        ),
    ]
