# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import GameRoom, Player, PlayerMove
from .utils import check_winner


class GameConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_name = None
        self.group_name = None
        self.room = None

    def connect(self):
        # print("Connected", self.scope["url_route"]["kwargs"]["room_name"])
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.group_name = self.room_name
        self.player_name = self.scope["query_string"].decode("utf-8").split("=")[-1]
        # print(self.player_name, self.scope)

        # Ensure that the room exists before accepting the connection
        try:
            self.room = GameRoom.objects.get(name=self.room_name)
        except GameRoom.DoesNotExist:
            # Handle the case where the room doesn't exist
            # For example, you could send an error message and close the connection
            self.close()
            return

        self.all_players = self.room.player_set.all()
        self.all_players = [player.name for player in self.all_players]

        # Accept the WebSocket connection
        self.accept()

        # Subscribe the consumer to the group
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name,
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)  # convert to python dict

        if text_data_json.get("type") == "start":
            # set the player's x turn to true
            player = Player.objects.get(game=self.room, name=self.player_name)

            player.is_turn = True
            player.save()

            # broadcast to group that a game creator just started game
            async_to_sync(self.channel_layer.group_send)(
                self.group_name, {"type": "start", "message": self.all_players}
            )
        elif text_data_json.get("type") == "join":
            # broadcast to group that a new player has joined
            async_to_sync(self.channel_layer.group_send)(
                self.group_name, {"type": "join", "message": self.all_players}
            )
        elif text_data_json.get("type") == "make_move":

            print(self.room, self.player_name)
            # get current player
            player = Player.objects.get(game=self.room, name=self.player_name)
            # print(player)

            # print(player.is_turn)
            # is is player's turn allow player to make move
            if player.is_turn:

                # get player move
                player_move = text_data_json.get("message")
                # update player move
                player_move_obj = PlayerMove.objects.create(
                    player=player, pos=player_move
                )
                print(player_move)  # print(text_data_json)
                player.switch_player_turn()  # switching player turn

                winner = check_winner(self.room)
                print(winner)

                async_to_sync(self.channel_layer.group_send)(
                    self.group_name,
                    {
                        "type": "make_move",
                        "message": player.symbol,
                        "move": player_move_obj.pos,
                        "is_turn": player.is_turn,
                    },
                )


    def join(self, event):
        self.send(text_data=json.dumps(event))

    def start(self, event):
        self.send(text_data=json.dumps(event))

    def make_move(self, event):
        self.send(text_data=json.dumps(event))

    def leave(self, event):
        self.send(text_data=json.dumps(event))
