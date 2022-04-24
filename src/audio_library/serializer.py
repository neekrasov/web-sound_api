from rest_framework import serializers

from . import models
from ..oauth.base.services import delete_old_file
from ..oauth.serializer import AuthorSerializer


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = ('id', 'title',)


class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.License
        fields = ('id', 'text',)


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Album
        fields = ('id', 'title', 'description', 'cover', 'private')

    def update(self, instance, validated_data):
        delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)


class CreateAuthorTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Track
        fields = (
            'user',
            'id',
            'title',
            'license',
            'genre',
            'album',
            'link_of_download',
            'file_to_download',
            'private',
            'cover',
            'created_at',
            'plays_count',
            'downoad_count',
        )
        read_only_fields = (
            'plays_count',
            'downoad_count',
            'user',
        )

    def update(self, instance, validated_data):
        delete_old_file(instance.file_to_download.path)
        delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)


class TrackSerializer(CreateAuthorTrackSerializer):
    license = LicenseSerializer()
    genre = GenreSerializer(many=True)
    album = AlbumSerializer()
    user = AuthorSerializer()


class CreatePlayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PlayList
        fields = ('id', 'title', 'cover', 'tracks')

    def update(self, instance, validated_data):
        delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)


class PlayListSerializer(CreatePlayListSerializer):
    tracks = TrackSerializer(many=True, read_only=True)


class CommentSerializer(serializers.ModelSerializer):
    user = AuthorSerializer()

    class Meta:
        model = models.Comment
        fields = ('id', 'text', 'user', 'track', 'created_at')


class CommentAuthorSerializer(serializers.ModelSerializer):
    """ Сериализация для CRUD комментариев автором """
    class Meta:
        model = models.Comment
        fields = ('id', 'text', 'track')
