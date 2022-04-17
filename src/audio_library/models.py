from django.core.validators import FileExtensionValidator
from django.db import models

from src.oauth.base.services import validate_size_image, get_path_upload_cover_album, get_path_upload_track, \
    get_path_upload_cover_playlist
from src.oauth.models import User


class License(models.Model):
    """ Модель лицензий треков пользователя """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='licenses')
    text = models.TextField(max_length=1024)


class Genre(models.Model):
    """ Модель жанров треков """
    title = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.title


class Album(models.Model):
    """ Модель альбомов для треков """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=1024)
    private = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to=get_path_upload_cover_album,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=('jpg',)), validate_size_image]
    )


class Track(models.Model):
    """ Модель треков """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tracks')
    title = models.CharField(max_length=128)
    license = models.ForeignKey(License, on_delete=models.CASCADE, related_name='license_tracks')
    genre = models.ManyToManyField(Genre, related_name='track_genres')
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, blank=True, null=True)
    link_of_download = models.CharField(max_length=512, blank=True, null=True)
    file_to_download = models.FileField(
        upload_to=get_path_upload_track,
        validators=[FileExtensionValidator(allowed_extensions=('wav', 'mp3'))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    plays_count = models.PositiveIntegerField(default=0)
    downoad_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    user_of_likes = models.ManyToManyField(User, related_name='likes_of_tracks')

    def __str__(self):
        return f'{self.user} - {self.title}'


class Comment(models.Model):
    """ Модель комментариев к треку """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='track_comments')
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)


class PlayList(models.Model):
    """ Модель плейлистов пользователя """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    title = models.CharField(max_length=64)
    tracks = models.ManyToManyField(Track, related_name='tracks_playlist')
    cover = models.ImageField(
        upload_to=get_path_upload_cover_playlist,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=('jpg',)), validate_size_image,]
    )

