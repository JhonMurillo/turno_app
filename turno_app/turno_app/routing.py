# from channels.routing import route
# from turnos.consumers import ws_connect, ws_disconnect


# channel_routing = [
#     route('websocket.connect', ws_connect),
#     route('websocket.disconnect', ws_disconnect),
# ]

# from channels.routing import ProtocolTypeRouter

# application = ProtocolTypeRouter({
#     # (http->django views is added by default)
# })

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import turnos.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            turnos.routing.websocket_urlpatterns
        )
    ),
})