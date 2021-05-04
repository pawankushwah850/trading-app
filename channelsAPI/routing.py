from channels.routing import URLRouter
from django.urls import re_path, path
from .consumers import UserConsumer

websocket_urlpatterns = URLRouter([
    path('ws/v1/', URLRouter([
        path('simple', UserConsumer.as_asgi()),
    ])),
])
