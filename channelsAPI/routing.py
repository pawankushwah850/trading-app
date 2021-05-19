from channels.routing import URLRouter
from django.urls import re_path, path
from .consumers import *

websocket_urlpatterns = URLRouter([
    path('ws/v1/', URLRouter([
        path('users', UserConsumer.as_asgi()),
        path('wallet', WalletConsumer.as_asgi()),
        path('asset', AssetConsumer.as_asgi()),
        path('notification', NotificationConsumer.as_asgi()),
    ])),
])
