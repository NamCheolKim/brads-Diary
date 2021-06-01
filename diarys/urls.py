from django.urls import path
from . import views

app_name = "diarys"

urlpatterns = [
    path("diary-list/", views.AlbumPostView.as_view(), name="list"),
    path("diary-detail/<int:pk>/", views.AlbumPostDetailView.as_view(), name="detail"),
    path("diary-create/", views.diary_create, name="create"),
    path("diary-modify/<int:pk>/", views.diary_modify, name="modify"),
    path("diary-delete/<int:pk>/", views.diary_delete, name="delete"),
    path("comment-create/<int:pk>/", views.create_comment, name="create_comment"),
    path("comment-modify/<int:pk>/", views.comment_modify, name="modify_comment"),
    path("comment-delete/<int:pk>", views.comment_delete, name="delete_comment"),
]
