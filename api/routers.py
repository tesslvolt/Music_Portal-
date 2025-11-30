from rest_framework.routers import DefaultRouter
from api.views import SongViewSet


router = DefaultRouter()
router.register(r'songs', SongViewSet, basename='songs')


