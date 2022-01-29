from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from .models import GameP2P


class GameP2PConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super(GameP2PConsumer, self).__init__(*args, capacity=2, **kwargs)
        self.game = None
        self.room_group_name = None

    def connect(self):
        kwargs = self.scope['url_route']['kwargs']
        if not self.scope['user'].is_authenticated:
            self.close()
            return
        self.game = GameP2P.game.get_game(self.scope['user'].id, kwargs['player2_id'])
        self.room_group_name = f'{self.game.id}{self.game.player1_id}{self.game.player2_id}'
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'player.join',
                'message': f'{self.scope["user"].username} joined the game',
                'user': self.scope['user'].username
            }
        )

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'player.left',
                'message': f'{self.scope["user"].username} has left',
                'user': self.scope['user'].username
            }
        )
        self.close()

    def receive_json(self, content, **kwargs):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                **content
            }
        )

    def player_move(self, event):
        self.send_json(event)

    def player_join(self, event):
        self.send_json(event)

    def player_left(self, event):
        self.send_json(event)

    def play_game(self, event):
        self.send_json(event)
