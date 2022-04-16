from rest_framework import viewsets, parsers, permissions

from .. import models, serializers
from ..base.permissions import IsAuthor


class UserView(viewsets.ModelViewSet):
    """ Просмотр и редактирование данных пользователя """
    parser_classes = (parsers.MultiPartParser,)
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.request.user

    def get_object(self):
        return self.get_queryset()


class AuthorView(viewsets.ReadOnlyModelViewSet):
    """ Список авторов """
    queryset = models.User.objects.all().prefetch_related('social_links')
    serializer_class = serializers.AuthorSerializer


class SocialLinkView(viewsets.ModelViewSet):
    """ CRUD ссылок соц.сетей пользователя """
    serializer_class = serializers.SocialLinkSerializer
    permission_classes = (IsAuthor,)

    def get_queryset(self):
        return self.request.user.social_links.all()

    def perform_create(self, serializer):  # !
        serializer.save(user=self.request.save())
