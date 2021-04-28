from django.urls import re_path

from investment.services import web_sockets_services

websocket_urlpatterns = [
    re_path(r'ws/$', web_sockets_services.ChatConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_name>\w+)/$', web_sockets_services.ChatConsumer.as_asgi()),

]