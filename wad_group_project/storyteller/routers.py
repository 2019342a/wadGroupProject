from swampdragon import route_handler
from swampdragon.route_handler import ModelRouter, BaseRouter

from django.contrib.auth.models import User
from storyteller.models import Story
from storyteller.serializers import StorySerializer

import random
import Queue

# Router for control of the story text
class StoryRouter(ModelRouter):
    route_name='story-router'
    serializer_class = StorySerializer
    model = Story

    def get_object(self, **kwargs):
        return self.model.objects.get(pk=kwargs['id'])

    def get_query_set(self, **kwargs):
        return self.model.objects.all()


# Router for control of the flow of the story room
class ControlRouter(BaseRouter):
    route_name='room-control-router'
    valid_verbs = ['add_user', 'remove_user', 'next_user', 'subscribe', 'unsubscribe', 'call_vote', 'vote_end', 'vote_dont_end', 'not_ending']

    def get_subscription_channels(self, **kwargs):
        return ['control']

    # Add a user to the story
    def add_user(self, **kwargs):
        new_user = User.objects.get(username=kwargs['user'])
        story = Story.objects.get(id=kwargs['storyid'])
        story.users.add(new_user)
        story.contributors.add(new_user)
        story.save()

    # Remove a user from the story
    def remove_user(self, **kwargs):
        old_user = User.objects.get(username=kwargs['user'])
        story = Story.objects.get(id=kwargs['storyid'])
        story.users.remove(old_user)
        if len(list(story.users.all())) == 0:
            story.curr_user = ""
        story.save()

    # Get the next user: sequentially if two, randomly if more than two
    def next_user(self, **kwargs):
        story = Story.objects.get(id=kwargs['storyid'])
        userslist = list(story.users.all())
        if len(userslist) != 0:
            if len(userslist) > 1:
                userslist.remove(User.objects.get(username=kwargs['prev_user']))
            rand_user = random.choice(userslist)
            story.curr_user = rand_user.username
            story.save()
        self.publish(self.get_subscription_channels(), {'comm': 'update-time'})

    # Get all connected users to show a voting dialog, restrict access to the story
    def call_vote(self, **kwargs):
        story = Story.objects.get(id=kwargs['storyid'])
        story.ending = True
        story.save()
        self.publish(self.get_subscription_channels(), {'comm': 'call-vote', 'sentence': kwargs['sentence']})

    # Accept a vote to end the story
    def vote_end(self, **kwargs):
        story = Story.objects.get(id=kwargs['storyid'])
        story.votes_to_end = story.votes_to_end + 1
        story.votes_counted = story.votes_counted + 1

        if story.votes_to_end > (story.users.count() / 2):
            story.story_text = story.story_text + " " + kwargs['sentence']
            self.publish(self.get_subscription_channels(), {'comm': 'end'})
            story.ended = True
        story.save()

    # Accept a vote to not end the story
    def vote_dont_end(self, **kwargs):
        story = Story.objects.get(id=kwargs['storyid'])
        story.votes_counted = story.votes_counted + 1

        if story.votes_counted == story.users.count():
            story.ending = False
            story.votes_counted = 0;
            story.votes_to_end = 0;
            self.publish(self.get_subscription_channels(), {'comm': 'resume'})
            story.ended = False
        story.save()



route_handler.register(StoryRouter)
route_handler.register(ControlRouter)
