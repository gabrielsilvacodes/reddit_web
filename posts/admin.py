from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Community, Post

admin.site.register(Community)
admin.site.register(Post)

