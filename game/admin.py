from django.contrib import admin
from .models import Player, GameRoom, PlayerMove

admin.site.register([GameRoom, Player, PlayerMove])