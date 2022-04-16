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


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SocialLink
        fields = ('id', 'link',)


class AuthorSerializer(serializers.ModelSerializer):
    social_links = SocialLinkSerializer(many=True)

    class Meta:
        model = models.User
        fields = ('id', 'avatar', 'country', 'city', 'bio', 'display_name', 'social_links')
