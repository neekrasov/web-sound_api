from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework.exceptions import AuthenticationFailed

from config import settings
from src.oauth import serializers
from src.oauth.models import User
from . import base_auth


def check_google_auth(google_user: serializers.GoogleAuth) -> dict:
    try:
        id_token.verify_oauth2_token(google_user['token'], requests.Request(), settings.GOOGLE_CLIENT_ID)
    except ValueError:
        raise AuthenticationFailed(code=403, detail='Bad token Google')

    user, _ = User.objects.get_or_create(email=google_user['email'])

    return base_auth.create_token(user.id)
