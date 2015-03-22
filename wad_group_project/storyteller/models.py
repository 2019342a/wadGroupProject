__author__ = 'Theofilos Alexiou'

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
    stories = models.IntegerField(default=0) 
    
    def save(self, *args, **kwargs):
            self.slug = slugify(self.name)
            super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


# This is the CompletedStory model. It has the information of the completed stories.
class CompletedStory(models.Model):  # See below 2
    completed_story_id = models.AutoField(primary_key=True, unique=True)  # See below 3
    views = models.IntegerField(default=0)  # we need the views for the top stories feature
    category = models.ForeignKey(Category)  # connection with Category model
    title = models.CharField(max_length=128)
    creator = models.ForeignKey(User)
    story_text = models.TextField()  # Stores large amounts of Text. See django documentation
    slug = models.SlugField()  # So it can be displayed on the url.
    rating = models.IntegerField(default=0)
    creation_date = models.DateTimeField(auto_now_add = True, editable=False)

    def save(self, *args, **kwargs):
            self.slug = slugify(self.completed_story_id)
            super(CompletedStory, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title


# This is the OngoingStory model. It has the information of the ongoing stories.
class OngoingStory(SelfPublishModel, models.Model):
    serializer_class = StorySerializer
    category = models.ForeignKey(Category)  # connection with Category model
    title = models.CharField(max_length=128)
    creator = models.CharField(max_length=128)
    story_text = models.TextField()  # Stores large amounts of Text. See django documentation
    users = models.ManyToManyField(User)  # Nice way of connected Many to Many without another table.
    contributors = models.ManyToManyField(User, related_name='contributorlist')
    curr_user = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)  # So it can be displayed on the url.
    creation_date = models.DateTimeField(auto_now_add = True, editable=False)
    
    def save(self, *args, **kwargs):
            self.slug = slugify(self.id)
            super(OngoingStory, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    
class Contributors(models.Model):
    contributor = models.ForeignKey(User)
    story = models.ForeignKey(CompletedStory)

#This is the Rating model. It has the ratings of a story
# class Rating(models.Model):
    # rating = models.IntegerField()  # Ratings will be from 1 to 10
    # rater = models.ForeignKey(User)  # Connection with User Model
    # story = models.ForeignKey(CompletedStory)  # Connection with Story model




# Comments:
# 1. We will probably wont need all these as we will use auth application
# or django-registration-redux or something similar
# 2. We are going to need two tables of Stories. One for completed and one for
# ongoing stories.The ongoing stories are connected with the users as it is in
# our specification. The completed stories are connected with the rating table.
# 3. Hopefully it will generate a unique id to use.
# 4. We will probably need a contributor attribute to Completed stories to display
# in our Wireframes.
# 5. In Rating model I didn't include a toString method as it asks for a String and
# we don't really need it. You will se the ratings in the database named as rating object.
# 6. In completedStory I removed the unique=True in slug because it raised an exception
# error. It might be the same in OngoingStory as I haven't populated it.
