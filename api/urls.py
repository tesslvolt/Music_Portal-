from django.urls import path
from api.views import test_api, SongListAPIView

urlpatterns = [
    path('test/', test_api),
    path('test/<int:pk>/', test_api),
    path('Song', SongListAPIView.as_view()),
]