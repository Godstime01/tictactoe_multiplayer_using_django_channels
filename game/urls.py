from django.urls import path
from . import views

urlpatterns = [
    path("join/<str:room_name>", views.join_room, name = 'game-room'),
    path("game/<str:room_name>", views.game_room, name = 'game-room'),
    path('', views.home_page, name = 'index'),
]
