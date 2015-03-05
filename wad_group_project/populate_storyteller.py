__author__ = 'Theofilos Alexiou'

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wad_group_project.settings')

import django
django.setup()

from storyteller.models import Category, User, CompletedStory, Rating


def populate():
    horror = add_cat('Horror')

    funny = add_cat('Funny')

    action = add_cat('Action')

    user1 = add_user('test1', 18, 'theofilosalexiou@gmail.com', 'test1')

    user2 = add_user('test2', 32, 'theofilosalexiou@gmail.com', 'test2')

    story1 = add_story(100, horror, 'scary1', 'test1', 'This is a test. Blah blah. Scary story')

    story2 = add_story(400, horror, 'scary2', 'test2', 'This is a test. Blah blah. Super scary story')

    story3 = add_story(50, funny, 'funny', 'test1', 'This is a test. Blah blah. funny story,'
                                                     ' <<insert funny sentence>>')

    rating1 = add_rating(5, user1, story2)

    rating1 = add_rating(8, user2, story1)


def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    return c


def add_user(name, age, email, password):
    u = User.objects.get_or_create(name=name, age=age, email=email, password=password)[0]
    return u


def add_story(views, category, title, creator, story_text):
    s = CompletedStory.objects.get_or_create(views=views, category=category, title=title, creator=creator,
                                   story_text=story_text)[0]
    return s


def add_rating(rating, rater, story):
    r = Rating.objects.get_or_create(rating=rating, rater=rater, story=story)[0]
    return r


# Start execution here!
if __name__ == '__main__':
    print "Starting storyteller population script..."
    populate()

# Comments:
# 1. I didn't populate the OngoingStory as it is dynamically populated.
# I can do some test though to test that everything works properly.