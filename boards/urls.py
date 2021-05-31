from django.urls import path
from . import views

app_name = "boards"

urlpatterns = [
    path("board-list/", views.board_list, name="list"),
]
