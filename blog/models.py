from django.db import models
from users.models import Profile
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from tinymce.models import HTMLField

from datetime import datetime, timedelta

class Post(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='post_pics', blank=True)
    content = HTMLField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, blank=True)
    changelog = models.TextField(max_length=5000)

    # Count likes (still a work in progress, using AJAX and lazy requests, no React yet)
    likes = models.ManyToManyField(User, related_name='blog_posts')

    # Count views
    blog_views=models.IntegerField(default=0)
    
    def total_likes(self):
        return self.likes.count()

    # Group
    Add_post_to_group = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class Publications(models.Model):
    title = models.CharField(max_length=100, blank=True)
    PDF = models.ImageField(upload_to='pub_pics', blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})




class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    write_comment = models.TextField(max_length=2000)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.author)

class City(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'cities'

class Ad(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='ad_pics', blank=True)
    content = models.CharField(max_length=500)
    Add_a_link = models.CharField(max_length=1000)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    ad_views=models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ad-detail', kwargs={'pk': self.pk})


class Market(models.Model):
    # FOR PRIVACY
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    enter_title = models.CharField(max_length=300)
    enter_price = models.IntegerField()
    Top_image_of_product = models.ImageField(upload_to='marketplace_pics', default="noimagefound.png")
    Image_2 = models.ImageField(upload_to='marketplace_pics', blank=True)
    Image_3 = models.ImageField(upload_to='marketplace_pics', blank=True)
    Image_4 = models.ImageField(upload_to='marketplace_pics', blank=True)
    Image_5 = models.ImageField(upload_to='marketplace_pics', blank=True)
    CONDITION_CHOICES = (
        (None, 'Condition:'),
        ('New', 'New'),
        ('Great', 'Great'),
        ('Good', 'Good'),
        ('Used', 'Used'),
        ('Damaged', 'Damaged'),
    )
    enter_condition = models.CharField(max_length=15, choices=CONDITION_CHOICES)
    Describe_product = models.TextField(max_length=500)
    enter_public_address = models.CharField(max_length=300)
    ITEM_TYPE_CHOICES = (
        (None, 'Item type:'),
        ('Single-List Item', 'Single-List Item'),
        ('Restocking', 'Restocking Item'),
    )
    enter_item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES)

    def __str__(self):
        return self.enter_title

    def get_absolute_url(self):
        return reverse('market-detail', kwargs={'pk': self.pk})
        