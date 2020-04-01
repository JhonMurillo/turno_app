import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from turnos.models import Turno

class TurnosConsumer(WebsocketConsumer):
    def connect(self):
        self.slug_identificador = self.scope['url_route']['kwargs']['slug_identificador']
        async_to_sync(self.channel_layer.group_add)(
            self.slug_identificador,
            self.channel_name
        )

        turnos_organizados = Turno.get_turnos(self.slug_identificador)

        # Send message to group
        async_to_sync(self.channel_layer.group_send)(
            self.slug_identificador,
            {
            'type': 'send_turnos',
            'turnos_organizados': turnos_organizados
            }
        )
        self.accept()
        print("#######CONNECTED############")


    def disconnect(self, close_code):
        print('Disconecting...', close_code)

    def receive(self, text_data):
        pass

    def send_turnos(self, event):
        print("#######SEDING MESSAGE############")
        turnos_organizados = event['turnos_organizados']
        # Send message to websocket
        self.send(text_data=json.dumps({
            'turnos_organizados': turnos_organizados
        }))
        print("#######MESSAGE SENT############")