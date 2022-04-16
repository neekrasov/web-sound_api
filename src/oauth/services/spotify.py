import base64
from typing import Optional

import requests
from rest_framework.exceptions import AuthenticationFailed

from config import settings
from src.oauth.models import User
from src.oauth.services import base_auth


def get_spotify_jwt(code: str) -> Optional[str]:
    url = 'https://accounts.spotify.com/api/token'
    basic_str = f'{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}'.encode('ascii')
    basic = base64.b64encode(basic_str)
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://localhost:3000/api/v1/auth/spotify-auth',
    }
    headers = {
        'Authorization': f'Basic {basic.decode("ascii")}'
    }

    response = requests.post(url, data=data, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        return response_json.get('access_token')
    else:
        return None


def get_spotify_user(token: str) -> str:
    url_get_user = 'https://api.spotify.com/v1/me'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url_get_user, headers=headers)
    response_json = response.json()
    return response_json.get('email')


def get_spotify_email(code: str) -> Optional[str]:
    _token = get_spotify_jwt(code)
    if _token is not None:
        return get_spotify_user(_token)
    else:
        return None


def spotify_auth(code: str):
    email = get_spotify_email(code)
    if email is not None:
        user, _ = User.objects.get_or_create(email=email)
        return base_auth.create_token(user_id=user.id)
    else:
        raise AuthenticationFailed(code=403, detail='Bad token Spotify')
