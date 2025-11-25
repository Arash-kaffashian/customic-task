from rest_framework import serializers
from .models import Mockup


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
            url = obj.image.url
            return request.build_absolute_uri(url) if request else url
        return ''
