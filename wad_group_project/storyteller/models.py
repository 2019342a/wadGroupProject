__author__ = 'Theofilos Alexiou'

from django.db import models
from django.template.defaultfilters import slugify


# This is the User model. It contains the basic information of a user
class User(models.Model):  # See below 1
    name = models.CharField(max_length=128, unique=True)
    age = models.IntegerField(default=None)
    email = models.EmailField(max_length=75)
    password = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)  # So it can be displayed on the url.

    def save(self, *args, **kwargs):
            self.slug = slugify(self.name)
            super(User, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


# This is the Category model. It contains all the categories.
class Category(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)  # So it can be displayed on the url.

    def save(self, *args, **kwargs):
            self.slug = slugify(self.name)
            super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


# This is the Story model. It has the information of the story.
class Story(models.Model):  # See below 2
    category = models.ForeignKey(Category)  # connection with Category model
    title = models.CharField(max_length=128)
    creator = models.CharField(max_length=128)
    story_text = models.TextField()  # Stores large amounts of Text. See django documentation
    slug = models.SlugField(unique=True)  # So it can be displayed on the url.

    def save(self, *args, **kwargs):
            self.slug = slugify(self.pk)  # It will display? the unique id.
            super(Story, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


# Writing model to connect many users with many stories
class Writing(models.Model):  # See below 3
    user_id = models.ForeignKey(User.pk)
    story_id = models.ForeignKey(Story.pk)

    def __unicode__(self):
        return self.name


# This is the Rating model. It has the ratings of a story
class Rating(models.Model):  # See below 4
    rating = models.FloatField()  # Ratings will be from 1.0 to 10.0
    rater = models.ForeignKey(User)  # Connection with User Model
    story = models.ForeignKey(Story)  # Connection with Story model

    def __unicode__(self):
        return self.name


# 1. We will probably wont need all these as we will use auth application
# or django-registration-redux or something similar
# 2. I have not included the User_id as I assume it is the unique primary key
# 3. I am not sure if this is the correct way to store the primary keys of the
# User and Story in the Writing model. The rango application does it different
# and does not access the primary key.
# 4. Same as three for connection. If you haven't noticed it is a Many-to-Many
# relationship for the User and Story models. As the tutor described it we need
# to have a ratings table and many users can rate many stories.