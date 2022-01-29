from django.urls import path
from .consumers import GameP2PConsumer

game_ws_urlpatterns = [
    path('ws/game/join/<int:player2_id>/', GameP2PConsumer.as_asgi()),
]
