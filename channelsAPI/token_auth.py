from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from jwt import decode as jwt_decode
from urllib.parse import parse_qs
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from django.conf import settings
import logging


@database_sync_to_async
def get_user(user_id):
    User = get_user_model()
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware:

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).
        print({
            'connection_type': scope.get('type', None),
            'request_url': scope.get('path', None),
            'browser_type': scope.get('headers', None)[5][1].decode("utf8"),
            'client_ip': ":".join(str(i) for i in scope.get('client', None)),
            'server_ip': ":".join(str(i) for i in scope.get('server', None)),
        })
        query = parse_qs(scope.get("query_string", None).decode("utf8")).get('token', None)
        token = None
        if query is not None:
            token = query[0]
            logging.info(f'Token : {token}')

            try:
                # This will automatically validate the token and raise an error if token is invalid
                UntypedToken(token)

            except (InvalidToken, TokenError) as e:
                # Token is invalid
                logging.error(e)

                return None
            else:
                #  Then token is valid, decode it
                decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                logging.info(decoded_data)

                scope['user'] = await get_user(int(decoded_data.get('user_id', None)))

                # Return the inner application directly and let it run everything else
        else:
            scope['user'] = await get_user(None)

        return await self.app(scope, receive, send)
