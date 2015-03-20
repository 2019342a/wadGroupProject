from django.contrib import admin
from storyteller.models import Category, UserProfile, CompletedStory, OngoingStory, Contributors

# Register your models here.

admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(CompletedStory)
admin.site.register(OngoingStory)
admin.site.register(Contributors)
