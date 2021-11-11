from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required()
def game_page(request):
    return render(request, "games/game.html")
