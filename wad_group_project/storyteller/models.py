from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

from storyteller.serializers import StorySerializer
from swampdragon.models import SelfPublishModel


# This is the User model. It contains the basic information of a user
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    age = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __unicode__(self):
        return self.user.username


# This is the Category model. It contains all the categories.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)  # So it can be displayed on the url.

    def save(self, *args, **kwargs):
            self.slug = slugify(self.name)
            super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


# This is the Story model. It has the information of the stories.
class Story(SelfPublishModel, models.Model):
    serializer_class = StorySerializer

    title = models.CharField(max_length=128)
    category = models.ForeignKey(Category)  # connection with Category model
    creator = models.CharField(max_length=128)
    story_text = models.TextField()  # Stores large amounts of Text. See django documentation
    contributors = models.ManyToManyField(User, related_name='contributorlist')
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    slug = models.SlugField(unique=True)  # So it can be displayed on the url.

    views = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)

    curr_user = models.CharField(max_length=128)
    users = models.ManyToManyField(User)  # Nice way of connected Many to Many without another table.

    ending = models.BooleanField(default=False)
    ended = models.BooleanField(default=False)
    votes_to_end = models.IntegerField(default=0)
    votes_counted = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
            self.slug = slugify(self.id)
            super(Story, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title
