from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

from games.models import Game


@receiver(post_save, sender=get_user_model())
def create_game_for_the_user(sender, instance, created, **kwargs):
    """Signal to create new game instance when user registers"""
    if created:
        Game.objects.create(user=instance)
