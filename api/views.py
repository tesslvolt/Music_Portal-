from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.serializers import SongSerializer
from app.models import Song


# Create your views here.
@api_view(['GET'])
def test_api(request):
    songs = Song.objects.all()
    genre = request.query_params.get('genre')
    if genre:
       songs = songs.filter(genre_id=genre)
    return Response([
        {
       'id': song.id,
       'title': song.title,
       'artist': song.artist.name,
        }
        for song in songs
    ])

class SongListAPIView(APIView):
    def get(self, request):
        songs = Song.objects.all()
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)




