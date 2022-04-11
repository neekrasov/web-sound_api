from rest_framework import serializers

from src.oauth import models


class GoogleAuthSerializer(serializers.Serializer):
    """ Сериализация данных от Google"""

    email = serializers.EmailField()
    token = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('avatar', 'country', 'city', 'bio', 'display_name',)
