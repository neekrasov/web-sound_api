import os

from django.http import FileResponse, Http404
from rest_framework import generics, viewsets, parsers, views
from rest_framework.generics import get_object_or_404

from . import models, serializer
from .serializer import TrackSerializer
from ..oauth.base.custom_classes import MixedSerializer, Pagination
from ..oauth.base.permissions import IsAuthor
from ..oauth.base.services import delete_old_file


class GenreView(generics.ListAPIView):
    """ Список жанров """
    queryset = models.Genre.objects.all()
    serializer_class = serializer.GenreSerializer


class LicenseView(viewsets.ModelViewSet):
    """ CRUD для лицензии автора """
    serializer_class = serializer.LicenseSerializer
    permission_classes = (IsAuthor,)

    def get_queryset(self):
        return models.License.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AlbumView(viewsets.ModelViewSet):
    """ CRUD альбомов автора """
    parser_classes = (parsers.MultiPartParser,)
    serializer_class = serializer.AlbumSerializer
    permission_classes = (IsAuthor,)

    def get_queryset(self):
        return models.Album.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        instance.delete()


class PublicAlbumView(generics.ListAPIView):
    serializer_class = serializer.AlbumSerializer

    def get_queryset(self):
        return models.Album.objects.filter(user__id=self.kwargs.get('pk'), private=False)


class TrackView(MixedSerializer, viewsets.ModelViewSet):
    """ CRUD треков пользователя """

    parser_classes = (parsers.MultiPartParser,)
    permission_classes = (IsAuthor,)
    serializer_class = serializer.CreateAuthorTrackSerializer
    serializer_classes_by_action = {
        'list': serializer.TrackSerializer
    }

    def get_queryset(self):
        return models.Track.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        instance.delete()


class PlayListView(MixedSerializer, viewsets.ModelViewSet):
    """ CRUD плейлистов пользователя """

    parser_classes = (parsers.MultiPartParser,)
    permission_classes = (IsAuthor,)
    serializer_class = serializer.CreatePlayListSerializer
    serializer_classes_by_action = {
        'list': serializer.PlayListSerializer
    }

    def get_queryset(self):
        return models.PlayList.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        instance.delete()


class AuthorTrackListView(generics.ListAPIView):
    """ Список треков автора """
    serializer_class = TrackSerializer
    pagination_class = Pagination

    def get_queryset(self):
        return models.Track.objects.filter(user__id=self.kwargs.get('pk'))  # Список треков по id автора


class TrackListView(generics.ListAPIView):
    """ Список всех треков """
    queryset = models.Track.objects.all()
    serializer_class = serializer.TrackSerializer
    pagination_class = Pagination


class StreamingFileView(views.APIView):

    def set_play(self, track):
        track.plays_count += 1
        track.save()

    def get(self, request, pk):
        track = get_object_or_404(models.Track, pk=pk)
        if os.path.exists(track.file_to_download.path):
            self.set_play(track)
            return FileResponse(open(track.file_to_download.path, 'rb'))
        else:
            return Http404


class DownloadTrackView(views.APIView):
    """ Скачивание трека """

    def set_download(self):
        self.track.downoad_count += 1
        self.track.save()

    def get(self, request, pk):
        self.track = get_object_or_404(models.Track, pk=pk)
        if os.path.exists(self.track.file_to_download.path):
            self.set_download()
            return FileResponse(open(self.track.file_to_download.path, 'rb'), filename=self.track.file_to_download.name,
                                as_attachment=True)  # as_attachment - заголовок для запуска загрузки в браузере
        else:
            return Http404
