from django.urls import path
from . import views

app_name = "diarys"

urlpatterns = [
    path("", views.index, name="index"),
    path("album/", views.AlbumPostView.as_view(), name="album"),
    path("detail/<int:pk>/", views.AlbumPostDetailView.as_view(), name="detail"),
    path("create/", views.AlbumPostCreateView.as_view(), name="create"),
]
