
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/play/', consumers.GameConsumer.as_asgi()),
    path('ws/play/<room_name>', consumers.GameConsumer.as_asgi()),
]