from django.contrib import admin
from storyteller.models import Category, User, CompletedStory, Rating, OngoingStory
# Register your models here.

admin.site.register(Category)
admin.site.register(User)
admin.site.register(CompletedStory)
admin.site.register(OngoingStory)
admin.site.register(Rating)