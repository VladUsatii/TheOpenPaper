# Generated by Django 3.0.8 on 2020-08-25 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0024_delete_videos'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
            options={
                'verbose_name_plural': 'cities',
            },
        ),
    ]