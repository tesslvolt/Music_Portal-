from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from app.models import Song, Album


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'title', 'album', 'genre', 'artist']


