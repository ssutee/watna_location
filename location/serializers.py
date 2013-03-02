from location.models import Location
from rest_framework import serializers

class MarkerSerializer(serializers.ModelSerializer):
    content = serializers.Field(source='info_window_content')
    color = serializers.Field(source='color')
    class Meta:
        model = Location
        fields = ('id', 'latitude', 'longitude', 'content', 'color',)