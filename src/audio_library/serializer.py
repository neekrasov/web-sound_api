from rest_framework import serializers
from . import models
from ..oauth.base.services import delete_old_file


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
    plays_count = serializers.IntegerField(read_only=True)
    downoad_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Track
        fields = (
            'id',
            'title',
            'license',
            'genre',
            'album',
            'link_of_download',
            'file_to_download',
            'created_at',
            'plays_count',
            'downoad_count',
        )

    def update(self, instance, validated_data):
        delete_old_file(instance.file_to_download.path)
        return super().update(instance, validated_data)


class TrackSerializer(CreateAuthorTrackSerializer):
    license = LicenseSerializer()
    genre = GenreSerializer(many=True)
    album = AlbumSerializer()


class CreatePlayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PlayList
        fields = ('id', 'title', 'cover', 'tracks')

    def update(self, instance, validated_data):
        delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)


class PlayListSerializer(CreatePlayListSerializer):
    tracks = TrackSerializer(many=True, read_only=True)