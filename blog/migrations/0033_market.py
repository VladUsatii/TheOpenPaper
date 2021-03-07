# Generated by Django 3.0.8 on 2020-08-29 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0032_post_blog_views'),
    ]

    operations = [
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enter_title', models.CharField(max_length=300)),
                ('enter_price', models.IntegerField()),
                ('Top_image_of_product', models.ImageField(default='noimagefound.png', upload_to='marketplace_pics')),
                ('Image_2', models.ImageField(blank=True, upload_to='marketplace_pics')),
                ('Image_3', models.ImageField(blank=True, upload_to='marketplace_pics')),
                ('Image_4', models.ImageField(blank=True, upload_to='marketplace_pics')),
                ('Image_5', models.ImageField(blank=True, upload_to='marketplace_pics')),
                ('enter_condition', models.CharField(choices=[(None, 'Condition:'), ('B', 'New'), ('G', 'Great'), ('F', 'Good'), ('U', 'Used'), ('D', 'Damaged')], max_length=1)),
                ('Describe_product', models.TextField(max_length=500)),
                ('enter_public_address', models.CharField(max_length=300)),
                ('enter_item_type', models.CharField(choices=[(None, 'Item type:'), ('1', 'Single-List Item'), ('2', 'Restocking Item')], max_length=1)),
            ],
        ),
    ]
