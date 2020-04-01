import os

from channels.asgi import get_channel_layer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'turno_app.settings')
application = get_channel_layer()