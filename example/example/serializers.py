from rest_framework import serializers
from example.models import Talk


class TalkSerializer (serializers.ModelSerializer):
    class Meta:
        model = Talk
        fields = ('topic', 'speaker', 'scheduled_at')
