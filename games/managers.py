from django.db.models import Q
from django.db.models.manager import Manager


class GameP2PManager(Manager):
    def get_game(self, player1_id: int, player2_id: int):
        try:
            game = self.model.objects.get(
                Q(player1_id=player1_id, player2_id=player2_id) |
                Q(player1_id=player2_id, player2_id=player1_id)
            )
        except self.model.DoesNotExist:
            print('Exception')
            game = self.model.objects.create(player1_id=player1_id, player2_id=player2_id)
        return game
