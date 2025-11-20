from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from app.views import register_view, main_view, audio_play, artist_view

urlpatterns = [
    path('', main_view, name='main'),
    path('register/', register_view, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('audio/<int:song_id>', audio_play, name='audio_play'),
    path('artist/<int:artist_id>/', artist_view, name='artist_detail')
]