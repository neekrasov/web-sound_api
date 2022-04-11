from google.auth.transport import requests
from google.oauth2 import id_token

from config import settings
from src.oauth import serializers
from src.oauth.models import User
from . import base_auth


def check_google_auth(google_user: serializers.GoogleAuthSerializer) -> dict:
    try:
        id_token.verify_oauth2_token(id_token=google_user['token'], request=requests.Request(),
                                     audience=settings.GOOGLE_CLIENT_ID)
    except ValueError:
        pass

    user, _ = User.objects.get_or_create(email=google_user['email'])

    return base_auth.create_token(user.id)
