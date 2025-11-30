from http.client import responses
from django.test import TestCase
from django.urls import reverse, resolve

from app.views import main_view, register_view, audio_play, artist_view
from django.contrib.auth.views import LoginView, LogoutView
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from app.models import Genre, Song, Artist, Album
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime


class RegisterViewTests(TestCase):
    def test_register_user(self):
        # словарь с обязательными полями формы
        form_data = {
            'username': 'alex',
            'password': '12345',
            'password2': '12345',
        }
        response = self.client.post(reverse('register'), data=form_data)
        # Проверяем редирект после успешной регистрации
        self.assertEqual(response.status_code, 302)
        # Проверяем, что пользователь реально создался
        self.assertTrue(User.objects.filter(username='alex').exists())

class MainViewTests(TestCase):
    def setUp(self):
        self.client = Client()\

        self.genre = Genre.objects.create(name = 'Rock')
        self.artist = Artist.objects.create(name = 'Artist 1')

        self.song1 = Song.objects.create(
            title="Song A",
            artist=self.artist,
            genre=self.genre,
            count=10,
            date=datetime.date(2024, 1, 1)
        )

        self.song2 = Song.objects.create(
            title="Song B",
            artist=self.artist,
            genre=self.genre,
            count=2,
            date=datetime.date(2024, 2, 1)
        )

    def test_main_page_loads(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Song A")
        self.assertContains(response, "Song B")

    def test_filter_by_genre(self):
        response = self.client.get(reverse('main'), {'genre': self.genre.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Song A")

    def test_search_query(self):
        response = self.client.get(reverse('main'), {'q': 'Song A'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Song A")

class ArtistViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.artist = Artist.objects.create(name = 'Eminem')

    def test_artist_page_loads(self):
        response = self.client.get(reverse('artist_detail', args=[self.artist.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Eminem")

class AudioViewTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username='test_name', password='123')

        self.file = SimpleUploadedFile(
            'test.mp3',
            b"fake-audio-data",
            content_type = "audio/mpeg"
        )

        artist = Artist.objects.create(name = 'Eazy-E')
        genre = Genre.objects.create(name = 'Rap')

        self.song = Song.objects.create(
            title="Test Song",
            artist=artist,
            genre=genre,
            audio_file=self.file
        )

    def test_audio_requires_login(self):
        response = self.client.get(reverse('audio_play', args=[self.song.id]))
        self.assertEqual(response.status_code, 302)

    def test_audio_play(self):
        self.client.login(username='test_name', password='123')
        response = self.client.get(reverse('audio_play', args=[self.song.id]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'audio/mpeg')


class ModelsTestCase(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="Pop")

        self.artist = Artist.objects.create(name="Artist")

        self.album = Album.objects.create(
            title="Album of Artist",
            artist=self.artist,
            release_year=2004
        )

        self.song = Song.objects.create(
            title="Song of Artist",
            artist=self.artist,
            album=self.album,
            genre=self.genre,
            count=300
        )

    def test_genre_creation(self):
        self.assertEqual(self.genre.name, "Pop")
        self.assertEqual(str(self.genre), "Pop")

    def test_artist_creation(self):
        self.assertEqual(self.artist.name, "Artist")
        self.assertEqual(str(self.artist), "Artist")


    def test_album_creation(self):
        self.assertEqual(self.album.title, "Album of Artist")
        self.assertEqual(self.album.artist, self.artist)
        self.assertEqual(str(self.album), "Album of Artist — Artist")


    def test_song_creation(self):
        self.assertEqual(self.song.title, "Song of Artist")
        self.assertEqual(self.song.artist, self.artist)
        self.assertEqual(self.song.album, self.album)
        self.assertEqual(self.song.genre, self.genre)
        self.assertEqual(self.song.count, 300)
        self.assertEqual(str(self.song), "Song of Artist — Artist")

class URLTests(TestCase):

    def test_main_url(self):
        url = reverse('main')
        self.assertEqual(url, '/')
        resolver = resolve(url)
        self.assertEqual(resolver.func, main_view)

    def test_register_url(self):
        url = reverse('register')
        self.assertEqual(url, '/register/')
        resolver = resolve(url)
        self.assertEqual(resolver.func, register_view)

    def test_login_url(self):
        url = reverse('login')
        self.assertEqual(url, '/login/')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, LoginView)

    def test_logout_url(self):
        url = reverse('logout')
        self.assertEqual(url, '/logout/')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, LogoutView)

    def test_audio_play_url(self):
        url = reverse('audio_play', args=[5])
        self.assertEqual(url, '/audio/5')
        resolver = resolve(url)
        self.assertEqual(resolver.func, audio_play)

    def test_artist_detail_url(self):
        url = reverse('artist_detail', args=[10])
        self.assertEqual(url, '/artist/10/')
        resolver = resolve(url)
        self.assertEqual(resolver.func, artist_view)

from django.test import TestCase
from app.forms import RegisterForm


class RegisterFormTests(TestCase):

    def test_valid_form(self):
        form = RegisterForm(data={
            'username': 'alex',
            'email': 'alex@example.com',
            'password': '12345',
            'password2': '12345'
        })
        self.assertTrue(form.is_valid())

    def test_passwords_do_not_match(self):
        form = RegisterForm(data={
            'username': 'alex',
            'email': 'alex@example.com',
            'password': '12345',
            'password2': '54321'
        })
        self.assertFalse(form.is_valid())
        self.assertIn("Пароли не совпадают", form.errors['__all__'])

    def test_missing_username(self):
        form = RegisterForm(data={
            'username': '',
            'email': 'alex@example.com',
            'password': '12345',
            'password2': '12345'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_missing_password2(self):
        form = RegisterForm(data={
            'username': 'alex',
            'email': 'alex@example.com',
            'password': '12345',
            'password2': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_missing_password(self):
        form = RegisterForm(data={
            'username': 'alex',
            'email': 'alex@example.com',
            'password': '',
            'password2': '12345'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)










