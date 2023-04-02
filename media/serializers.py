from rest_framework import serializers
from .models import Channel, Content


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'


class ChannelSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True)
    subchannels = serializers.SerializerMethodField()

    def get_subchannels(self, obj):
        return ChannelSerializer(obj.subchannels.all(), many=True).data

    class Meta:
        model = Channel
        fields = '__all__'
