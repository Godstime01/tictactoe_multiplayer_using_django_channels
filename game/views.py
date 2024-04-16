from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import GameRoom, Player, PlayerMove


def home_page(request):
    if request.method == "POST":
        # Get the room name from the POST request
        player_name = request.POST.get("room_name", "")
        # Create a new GameRoom object with the provided name
        new_room = GameRoom.objects.create(name=None)
        player = Player.objects.create(name=player_name, game=new_room, symbol="X")

        reversed_url = reverse_lazy("game-room", kwargs={"room_name": new_room.name})

        # Redirect to the game room page with the room name as a parameter
        return HttpResponseRedirect(f"{reversed_url}?player_name={player.name}")

    return render(request, "index.html", {})


def game_room(request, room_name):
    user = request.GET.get('player_name', '')
    
    room_name, created = GameRoom.objects.get_or_create(name=room_name)
    player = Player.objects.get(name = user)
    print(room_name.num_of_participant())

    return render(request, "game_room.html", {"room": room_name, 'player': player})


def join_room(request, room_name):

    room_name = get_object_or_404(GameRoom, name=room_name)

    if request.method == "POST":
        player_name = request.POST.get("room_name", "")
        # Create a new GameRoom object with the provided name

        if room_name.check_max():
            messages.error(request, 'Maximum of 2 players, create a new game')
            return redirect('index')

        player = Player.objects.create(
            name=player_name, game=room_name, symbol="O", is_creator=False
        )

        reversed_url = reverse_lazy(
            "game-room", kwargs={"room_name": room_name.name}
        )

        # Redirect to the game room page with the room name as a parameter
        return HttpResponseRedirect(f"{reversed_url}?player_name={player.name}")

    return render(request, "join_game.html", {"room": room_name})
