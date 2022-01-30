from typing import Optional

from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from accounts.models import CustomUser

from .decorators import timeit
from .models import Winner, Cell, Game, GameP2P
from .game import computer_move, check_winner


@timeit
@login_required()
def change_symbol(request):
    game: Game = request.user.game
    game.change_symbol()
    return HttpResponse(game.symbol)


@timeit
@login_required()
def game_with_player_view(request, username=None):
    if username:
        player2 = get_object_or_404(CustomUser.objects.only('id'), username=username)
        game: GameP2P = GameP2P.game.get_game(request.user.id, player2.id)
        if game.player1_id == request.user.id:
            you = {'symbol': game.player1_symbol, 'wins': game.player1_wins}
            opponent = {'symbol': game.player2_symbol, 'wins': game.player2_wins}
        else:
            you = {'symbol': game.player2_symbol, 'wins': game.player2_wins}
            opponent = {'symbol': game.player1_symbol, 'wins': game.player2_wins, 'id': player2.id}
        opponent.update({'id': player2.id})
        return render(request, 'games/game_with_player.html', {
            'username': username, 'game': game, 'you': you, 'opponent': opponent
        })
    return render(request, 'games/game_with_player.html')


@timeit
@login_required()
def game_with_computer_view(request):
    return render(request, 'games/game_with_computer.html')


@timeit
@login_required()
def game_page(request):
    return render(request, "games/game.html")


@csrf_exempt
@require_POST
@login_required()
@timeit
def make_a_move_view(request):
    game: Game = request.user.game

    # If game is already over then return response
    if game.winner:
        return HttpResponseNotAllowed("Game is already over")

    if "computerFirst" in request.POST:
        com_move = computer_move(game)
        win_status = None
    else:
        row, col = int(request.POST["row"]), int(request.POST["col"])
        game = game.make_a_move(Cell(row, col), Winner.PLAYER1)
        win_status = check_winner(game)
        com_move: Optional[Cell] = None
        if not win_status and game.moves_left > 0:
            com_move = computer_move(game)
            win_status = check_winner(game)

        if win_status:
            game.save_winner(win_status.winner)

    return JsonResponse({
        "player": game.symbol,
        "com_position": com_move._asdict() if com_move else None,
        "win_status": win_status.to_json() if win_status else None
    })


@timeit
@login_required()
def new_game_with_computer_view(request):
    request.user.game.new_game()
    return redirect("computer_game")
