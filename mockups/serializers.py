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
            # orange code : files must be stay files ? or what ?
            relative_url = obj.image.url.replace('/media/', '/files/')
            if request:
                return request.build_absolute_uri(relative_url)
            return relative_url
        return ''



