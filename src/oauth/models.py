from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import Permission, PermissionsMixin
from django.core.validators import FileExtensionValidator
from django.db import models

from src.oauth.base.services import get_path_upload_avatar, validate_size_image
from src.oauth.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    """ Модель пользователя """
    email = models.EmailField(max_length=150, unique=True)
    join_date = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(max_length=2000, blank=True, null=True)
    display_name = models.CharField(max_length=30, blank=True, null=True)
    avatar = models.ImageField(
        upload_to=get_path_upload_avatar,
        blank=True,
        null=True,
        validators=(FileExtensionValidator(allowed_extensions=('jpg',)), validate_size_image,)
    )

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    @property
    def is_authenticated(self):
        """ Аутентифицирован ли пользователь """
        return True

    def __str__(self):
        return self.email


class Follower(models.Model):
    """ Модель подписчика """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribers')

    def __str__(self):
        return f'{self.subscriber} subscribed to {self.user}'


class SocialLink(models.Model):
    """ Модель ссылок на соц.сети пользователя """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_links')
    link = models.URLField(max_length=100)

    def __str__(self):
        return f'{self.user}'
