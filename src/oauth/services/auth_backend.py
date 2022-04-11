from datetime import datetime
from typing import Union

import jwt
from rest_framework import authentication, exceptions

from config import settings
from src.oauth.models import User


class AuthBackend(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request, token=None, **kwargs) -> Union[None, tuple]:
        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header or auth_header[0].lower() != b'token':
            return None

        if len(auth_header) == 1:
            raise exceptions.AuthenticationFailed('Inavlid token header. No credential provided.')
        elif len(auth_header) > 2:
            raise exceptions.AuthenticationFailed('Invalid token header. Token string dhould not contain spaces.')

        try:
            token = auth_header[1].decode('utf-8')
        except UnicodeError:
            raise exceptions.AuthenticationFailed(
                'Invalid token header. Token string should not contain invalid characters.')

        return self.authenticate_credential(token)

    def authenticate_credential(self, token) -> tuple:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        except jwt.PyJWTError:
            raise exceptions.AuthenticationFailed('Invalid authentication. Could not decode token.')

        token_exp = datetime.fromtimestamp(payload['exp'])
        if token_exp < datetime.utcnow():
            raise exceptions.AuthenticationFailed('Token expired')

        try:
            user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No user mathing this token was found.')

        return user, None  # user -> request, None -> request.auth
