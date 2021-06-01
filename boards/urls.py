from django.urls import path
from . import views

app_name = "boards"

urlpatterns = [
    path("board-list/", views.BoardListView.as_view(), name="list"),
]
