from swampdragon import route_handler
from swampdragon.route_handler import ModelRouter, BaseRouter

from django.contrib.auth.models import User
from storyteller.models import OngoingStory
from storyteller.serializers import StorySerializer

import random
import Queue

class StoryRouter(ModelRouter):
    route_name='story-router'
    serializer_class = StorySerializer
    model = OngoingStory
    
    def get_object(self, **kwargs):
        return self.model.objects.get(pk=kwargs['id'])

    def get_query_set(self, **kwargs):
        return self.model.objects.all()


class ControlRouter(BaseRouter):
    route_name='room-control-router'
    valid_verbs = ['add_user', 'remove_user', 'next_user', 'subscribe']
    
    def get_subscription_channels(self, **kwargs):
        return ['control']
    
    def add_user(self, **kwargs):
        new_user = User.objects.get(username=kwargs['user'])
        story = OngoingStory.objects.get(id=kwargs['storyid'])
        story.users.add(new_user)
        story.contributors.add(new_user)
        story.save()

    def remove_user(self, **kwargs):
        old_user = User.objects.get(username=kwargs['user'])
        story = OngoingStory.objects.get(id=kwargs['storyid'])
        story.users.remove(old_user)
        if len(list(story.users.all())) == 0:
            story.curr_user = ""
        story.save()

    def next_user(self, **kwargs):
        story = OngoingStory.objects.get(id=kwargs['storyid'])
        userslist = list(story.users.all())
        if len(userslist) != 0:
            if len(userslist) > 1:
                userslist.remove(User.objects.get(username=kwargs['prev_user']))
            rand_user = random.choice(userslist)
            story.curr_user = rand_user.username
            story.save()
        self.publish(self.get_subscription_channels(), {'update-time': True})

        
        
route_handler.register(StoryRouter)
route_handler.register(ControlRouter)

