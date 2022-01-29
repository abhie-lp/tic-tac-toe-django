from django.db.models import Q
from django.db.models.manager import Manager


class GameP2PManager(Manager):
    def get_game(self, player1, player2):
        try:
            game = self.model.objects.get(
                Q(player1=player1, player2=player2) |
                Q(player1=player2, player2=player1)
            )
        except self.model.DoesNotExist:
            print('Exception')
            game = self.model.objects.create(player1=player1, player2=player2)
        return game
