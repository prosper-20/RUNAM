from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
    re_path(r'ws/chat/room/(?P<task_id>\w{8}-\w{4}-\w{4}-\w{4}-\w{12})/$',consumers.ChatConsumer.as_asgi()),
]