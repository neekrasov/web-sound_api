from rest_framework import serializers
from . import models


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = ('id', 'title',)


class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.License
        fields = ('id', 'text',)
