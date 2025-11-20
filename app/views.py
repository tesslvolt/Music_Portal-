from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, Http404
import os
from app.forms import RegisterForm
from app.models import Genre, Song, Artist
from django.shortcuts import get_object_or_404, render
from .models import Artist

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # хэшируем пароль
            user.save()
            user = authenticate(username=user.username, password=form.cleaned_data['password'])

            if user:
                login(request, user)  # сразу авторизуем пользователя
            return redirect('main')  # редирект на главную
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def main_view(request):
    genres = Genre.objects.all() # выгрузка из таблицы жанры
    genre_id = request.GET.get('genre') 
    query = request.GET.get('q')
    songs = Song.objects.all()

    top_songs = songs.order_by('-count')[:3]
    new_songs = songs.order_by('-date')[:3]

    if genre_id:
        songs = songs.filter(genre_id=genre_id)
    if query:
        songs = songs.filter(
            Q(title__icontains=query) |
            Q(artist__name__icontains=query)
        )

    return render(request, 'main.html', {
        'songs': songs,
        'top_songs': top_songs,
        'new_songs': new_songs,
        'genres': genres,
        'selected_genre': genre_id
    })


@login_required(login_url='/login/')
def audio_play(request, song_id):
    try:
        song = Song.objects.get(id=song_id)

        song.count = (song.count or 0) + 1
        song.save(update_fields=['count'])

        if not song.audio_file:
            raise Http404("Аудиофайл отсутствует")

        file_path = song.audio_file.path

        if not os.path.exists(file_path):
            raise Http404("Файл не найден")

        return FileResponse(open(file_path, 'rb'), content_type='audio/mpeg')

    except Song.DoesNotExist:
        raise Http404("Песня не найдена")


def artist_view(request, artist_id):
    artist = Artist.objects.get(pk=artist_id)
    albums = artist.albums.all()
    songs = artist.songs.all()

    return render(request, 'artist.html', {
        'artist': artist,
        'albums': albums,
        'songs': songs,
    })










