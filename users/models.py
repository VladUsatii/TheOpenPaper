from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    Choose_banner = models.ImageField(default='default_banner.png', upload_to='banner_pics')
    About_you = models.CharField(max_length=19999999, blank=True)
    Write_your_bio = models.TextField(max_length=500, blank=True)
    Add_an_education_credential = models.CharField(max_length=200, blank=True)
    Add_current_title = models.CharField(max_length=200, blank=True)
    Add_current_employer = models.CharField(max_length=200, blank=True)
    Home_details = models.CharField(max_length=199999, blank=True)
    Current_city = models.CharField(max_length=200, blank=True)
    Current_address = models.CharField(max_length=300, blank=True)
    Add_hometown = models.CharField(max_length=300, blank=True)

    GENDER_CHOICES = (
        (None, 'Sex:'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )
    Choose_gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)

    External_links = models.CharField(max_length=19999, blank=True)
    Add_Facebook = models.CharField(max_length=100, blank=True)
    Add_Twitter = models.CharField(max_length=100, blank=True)
    Add_YouTube = models.CharField(max_length=100, blank=True)
    Add_Instagram = models.CharField(max_length=100, blank=True)
    Add_your_personal_website =  models.CharField(max_length=300, blank=True)

    verified = models.BooleanField(default=False)
    ad = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        img = Image.open(self.image.path)
        img2 = Image.open(self.Choose_banner.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

        if img2.height > 624 or img2.width > 1640:
            output_size = (1640, 624)
            img2.thumbnail(output_size)
            img2.save(self.Choose_banner.path)
