from rest_framework import generics, viewsets
from . import models, serializer
from ..oauth.base.permissions import IsAuthor


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
