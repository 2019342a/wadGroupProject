from swampdragon.serializers.model_serializer import ModelSerializer

class StorySerializer(ModelSerializer):
    class Meta:
        model = 'storyteller.OngoingStory'
        publish_fields = ('title', 'story_text', 'curr_user')
        update_fields = ('story_text')
