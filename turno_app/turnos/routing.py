from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/turnos/(?P<slug_identificador>\w+)/$', consumers.TurnosConsumer),
]