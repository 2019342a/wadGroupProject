from django.contrib import admin
from storyteller.models import Category, UserProfile, Story
# Register your models here.

admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(Story)
