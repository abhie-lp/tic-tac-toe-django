from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required()
def change_symbol(request):
    symbol = request.user.game.symbol
    if symbol == "X":
        symbol = "0"
    else:
        symbol = "X"
    request.user.game.symbol = symbol
    request.user.game.save()
    return HttpResponse(symbol)


@login_required()
def game_page(request):
    return render(request, "games/game.html")
