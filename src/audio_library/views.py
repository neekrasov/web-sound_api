import os

from django.http import FileResponse, Http404, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
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
        delete_old_file(instance.file_to_download.path)
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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'album__title', 'genre__title']

    def get_queryset(self):
        return models.Track.objects.filter(user__id=self.kwargs.get('pk'), album__private=False,
                                           private=False)  # Список треков по id автора


class TrackListView(generics.ListAPIView):
    """ Список всех треков """
    queryset = models.Track.objects.filter(album__private=False, private=False)
    serializer_class = serializer.TrackSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'user__display_name', 'album__title', 'genre__title']


class CommentAuthorView(viewsets.ModelViewSet):
    """ CRUD комментариев автора """

    serializer_class = serializer.CommentAuthorSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return models.Comment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentView(viewsets.ModelViewSet):
    """ Комментарии к треку """

    serializer_class = serializer.CommentSerializer

    def get_queryset(self):
        return models.Comment.objects.filter(track__id=self.kwargs['pk'])


class StreamingFileView(views.APIView):

    def set_play(self):
        self.track.plays_count += 1
        self.track.save()

    def get(self, request, pk):
        self.track = get_object_or_404(models.Track, pk=pk, private=False)
        if os.path.exists(self.track.file_to_download.path):
            self.set_play()
            response = HttpResponse('', content_type="audio/mpeg", status=206)
            response['X-Accel-Redirect'] = f"/mp3/{self.track.file_to_download.name}"
            return response
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
            response = HttpResponse('', content_type='audio/mpeg', status=206)
            response["Content-Disposition"] = f"attachment; filename={self.track.file_to_download.name}"
            response["X-Accel-Redirect"] = f"/media/{self.track.file_to_download.name}"
        else:
            return Http404


class StreamingFileAuthorView(views.APIView):
    permission_classes = [IsAuthor]

    def get(self, request, pk):
        self.track = get_object_or_404(models.Track, pk=pk, user=request.user)
        if os.path.exists(self.track.file_to_download.path):
            response = HttpResponse('', content_type="audio/mpeg", status=206)
            response['X-Accel-Redirect'] = f"/mp3/{self.track.file_to_download.name}"
            return response
        else:
            return Http404
