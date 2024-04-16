import uuid
from django.db import models


class GameRoom(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True, unique=True)

    def save(self, *args, **kwargs):
        # If the name is not provided explicitly, generate a new name
        if not self.name:
            self.name = self.generate_name()
        super().save(*args, **kwargs)

    def generate_name(self):
        return f"Game-{uuid.uuid4().hex[:8]}"
    
    def check_max(self):
        return self.player_set.count() == 2
    
    def num_of_participant(self):
        len(['' for _ in self.player_set.all()])
        return str(2)

    def __str__(self):
        return self.name
    

class Player(models.Model):
    game = models.ForeignKey(GameRoom, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    symbol = models.CharField(max_length=1)
    is_creator = models.BooleanField(default=True)
    is_turn = models.BooleanField(default=False)

    def switch_player_turn(self):
        # Get the other player in the game
        other_player = self.game.player_set.exclude(id=self.id).first()
        if other_player:
            # Switch turns
            self.is_turn = not self.is_turn
            other_player.is_turn = not other_player.is_turn
            self.save()
            other_player.save()

    def __str__(self):
        return self.name + self.symbol
    

class PlayerMove(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    pos = models.IntegerField()

    def __repr__(self):
        return f"{self.pos}"