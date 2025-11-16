from rest_framework import serializers
from .models import Mockup, GenerationTask


# MOCKUP LIST SERIALIZER
class MockupSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Mockup
        fields = ('id', 'text', 'font', 'text_color', 'shirt_color', 'image_url', 'created_at')

    # IMAGE URL GENERATOR FOR EACH TASK
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            relative_url = obj.image.url.replace('/media/', '/files/')
            if request:
                return request.build_absolute_uri(relative_url)
            return relative_url
        return ''


# TASK LIST SERIALIZER
class GenerationTaskSerializer(serializers.ModelSerializer):
    # green code : why result ? how it is work ?
    results = MockupSerializer(many=True, read_only=True)

    class Meta:
        model = GenerationTask
        fields = ('task_id', 'status', 'created_at', 'results')
