import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

from channelsAPI.routing import websocket_urlpatterns
from channelsAPI.token_auth import TokenAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VirtualCurruncy.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": TokenAuthMiddleware(
        URLRouter([
            path("virtualcoin/", websocket_urlpatterns),
        ])
    ),
})
