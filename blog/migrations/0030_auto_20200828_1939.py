# Generated by Django 3.0.8 on 2020-08-28 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0029_ad'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='Ad_link',
            field=models.CharField(default=1, max_length=1000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ad',
            name='content',
            field=models.CharField(max_length=500),
        ),
    ]
