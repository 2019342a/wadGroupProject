__author__ = 'Theofilos Alexiou'

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wad_group_project.settings')

import django
django.setup()

from storyteller.models import Category, UserProfile, Story
from django.contrib.auth.models import User

def populate():

    # -------------------------------------------
    #      Populate user and profile table
    # -------------------------------------------

    test = add_user('test', 18, 'test@test.com', 'test')

    test2 = add_user('test2', 32, 'theofilosalexiou@gmail.com', 'test2')

    newuser = add_user('newuser', 19, 'fake@gmail.com', 'password')

    neweruser = add_user('neweruser', 18, 'stories@gmail.com', 'secret')


    # -------------------------------------------
    #           Populate category table
    # -------------------------------------------

    horror = add_cat('Horror')

    comedy = add_cat('Comedy')

    action = add_cat('Action')

    drama = add_cat('Drama')


    # -------------------------------------------
    #             Populate story table
    # -------------------------------------------

    # Completed stories
    add_completed_story(100, horror, 'Scary Story', 'test', 'This is a test. Blah blah. Scary story.', 0, [test.user, test2.user])

    add_completed_story(400, horror, 'Mr skeltal', 'test2', 'This is a test. Blah blah. Super scary story', 5, [test2.user, newuser.user])

    add_completed_story(50, comedy, 'Funny Story', 'neweruser', 'This is a test. Blah blah. Funny story. Funny sentence.', 8, [neweruser.user, test2.user])

    add_completed_story(39, action, 'Action Story', 'newuser', 'Action story first sentence. Second sentence continuing the story. Third sentence.', 4, [newuser.user, test.user, test2.user])

    # Ongoing Stories
    add_ongoing_story(drama, 'Drama Story', 'newuser', 'Drama story. New sentences can be submitted to add to this.', [newuser.user, test.user])

    add_ongoing_story(action, 'Action Story 2', 'test2', 'Action! Stuff happening... New sentences added.', [test.user, test2.user])



def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    return c


def add_user(name, age, email, password):
    new_user = User.objects.create_user(name, email, password)
    u = UserProfile.objects.get_or_create(age=age, user=new_user)[0]
    return u


def add_completed_story(views, category, title, creator, story_text, rating, contributors):
    s = Story.objects.get_or_create(views=views, category=category, title=title, creator=creator,
                                   story_text=story_text, rating = rating, ending=True, ended=True)[0]
    for add_contributor in contributors:
        s.contributors.add(add_contributor)
    s.save();
    return s

def add_ongoing_story(category, title, creator, story_text, contributors):
    s = Story.objects.get_or_create(category=category, title=title, creator=creator,
                                   story_text=story_text, ended=False)[0]
    for add_contributor in contributors:
        s.contributors.add(add_contributor)
    s.save()
    return s


# Start execution here!
if __name__ == '__main__':
    print "Starting storyteller population script..."
    populate()
