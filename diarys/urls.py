from django.urls import path
from . import views

app_name = "diarys"

urlpatterns = [
    path("diary-list/", views.AlbumPostView.as_view(), name="list"),
    path("diary-detail/<int:pk>/", views.AlbumPostDetailView.as_view(), name="detail"),
    path("diary-create/", views.diary_create, name="create"),
    path("diary-modify/<int:pk>", views.diary_modify, name="modify"),
    path("diary-delete/<int:pk>", views.diary_delete, name="delete"),
]
