import os

from django.core.exceptions import ValidationError


def get_path_upload_avatar(instance, file_path):
    """ Построение пути к файлу.
        format: (media)/avatar/user_id/photo.jpg
        instance: User
        file: photo.jpg
    """
    return f'avatar/user_{instance.id}/{file_path}'


def get_path_upload_cover_album(instance, file_path):
    """ Построение пути к файлу.
        format: (media)/album/user_id/photo.jpg
        instance: User
        file: photo.jpg
    """
    return f'album/user_{instance.user.id}/{file_path}'


def get_path_upload_track(instance, file_path):
    """ Построение пути к файлу.
        format: (media)/track/user_id/audio.mp3
        instance: User
        file: photo.jpg
    """
    return f'track/user_{instance.user.id}/{file_path}'


def get_path_upload_cover_track(instance, file_path):
    """ Построение пути к файлу.
        format: (media)/track/user_id/photo.jpg
        instance: User
        file: photo.jpg
    """
    return f'track/cover/user_{instance.user.id}/{file_path}'


def get_path_upload_cover_playlist(instance, file_path):
    """ Построение пути к файлу.
        format: (media)/playlist/user_id/photo.jpg
        instance: User
        file: photo.jpg
    """
    return f'playlist/user_{instance.user.id}/{file_path}'


def validate_size_image(file_obj):
    """ Проверка размера файла """
    limit = 2  # MB
    if file_obj.size > limit * 1024 * 1024:
        raise ValidationError(f"File size exceeds {limit} MB")


def delete_old_file(file_path):
    """ Удаление старого файла """

    if os.path.exists(file_path):
        os.remove(file_path)
