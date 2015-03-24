from django import forms
from django.contrib.auth.models import User
from storyteller.models import UserProfile, Story

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('age', 'picture')

class StoryForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Title")
    class Meta:
        model = Story
        fields = ('title', 'category')
