from typing import Optional

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from accounts.models import CustomUser
from .game import check_winner, GameStatus
from .models import GameP2P, Cell, Winner


class GameP2PConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super(GameP2PConsumer, self).__init__(*args, capacity=2, **kwargs)
        self.game: Optional[GameP2P] = None
        self.room_group_name: Optional[str] = None
        self.user: Optional[CustomUser] = None
        self.my_move: Optional[Winner] = None
        self.other_move: Optional[Winner] = None

    def connect(self):
        if not self.scope['user'].is_authenticated:
            self.close()
            return
        self.user = self.scope['user']
        self.game = GameP2P.game.get_game(self.user.id,
                                          self.scope['url_route']['kwargs']['player2_id'])
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
                'message': f'{self.user.username} joined the game',
                'user': self.user.username
            }
        )
        if self.user.id == self.game.player1_id:
            self.my_move, self.other_move = Winner.PLAYER1, Winner.PLAYER2
        else:
            self.my_move, self.other_move = Winner.PLAYER2, Winner.PLAYER1

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'player.left',
                'message': f'{self.user.username} has left',
                'user': self.user.username
            }
        )
        self.close()

    def receive_json(self, content, **kwargs):
        action = content['type']
        if action == 'change.symbol':
            content.update(self.handle_change_symbol())
        elif action == 'player.move':
            content = self.handle_player_move(content)
        elif action == 'new.game':
            self.handle_new_game()
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                **content,
            }
        )

    def handle_player_move(self, content: dict) -> dict:
        self.game = self.game.make_a_move(
            Cell(int(content['row']), int(content['col'])), self.my_move
        )
        winner: GameStatus = check_winner(self.game, self.my_move, self.other_move)
        if winner:
            content['type'] = 'game.over'
            content['win'] = winner.to_json()
            self.game.save_winner(winner.winner)
            content[self.game.player1_username] = self.game.player1_wins
            content[self.game.player2_username] = self.game.player2_wins
        return content

    def player_move(self, event):
        self.send_json(event)

    def player_join(self, event):
        self.send_json(event)

    def player_left(self, event):
        self.send_json(event)

    def play_game(self, event):
        self.send_json(event)

    def handle_change_symbol(self) -> dict:
        self.game = self.game.change_symbol()
        return {self.game.player1_username: self.game.player1_symbol,
                self.game.player2_username: self.game.player2_symbol}

    def change_symbol(self, event):
        self.send_json(event)

    def game_over(self, event):
        self.send_json(event)

    def handle_new_game(self):
        self.game.new_game()

    def new_game(self, event):
        self.send_json(event)
