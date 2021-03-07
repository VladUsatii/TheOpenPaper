from django.contrib import admin
from .models import Post, City, Ad, Market, Comment

admin.site.register(City)
admin.site.register(Ad)
admin.site.register(Market)
admin.site.register(Post)
admin.site.register(Comment)