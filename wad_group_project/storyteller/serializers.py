from swampdragon.serializers.model_serializer import ModelSerializer

class StorySerializer(ModelSerializer):
    class Meta:
        model = 'storyteller.Story'
        publish_fields = ('title', 'story_text', 'curr_user', 'creator', 'ended')
        update_fields = ('story_text')
