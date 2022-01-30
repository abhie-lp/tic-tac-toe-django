from django.db.models import Q, F
from django.db.models.manager import Manager


class GameP2PManager(Manager):
    def get_game(self, player1_id: int, player2_id: int):
        try:
            game = self.model.objects \
                .annotate(player1_username=F('player1__username'),
                          player2_username=F('player2__username')) \
                .defer('created') \
                .get(
                    Q(player1_id=player1_id, player2_id=player2_id) |
                    Q(player1_id=player2_id, player2_id=player1_id)
                )
        except self.model.DoesNotExist:
            print('Exception')
            game = self.model.objects.create(player1_id=player1_id, player2_id=player2_id)
        return game
