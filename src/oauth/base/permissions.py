from rest_framework import permissions


class IsAuthor(permissions.IsAuthenticated):
    """ Проверка отправившего запрос юзера на авторство записи в базе данных """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
