from django.urls import path
from . import views

app_name = "diarys"

urlpatterns = [
    path("diary-list/", views.AlbumPostView.as_view(), name="list"),
    path("diary-detail/<int:pk>/", views.AlbumPostDetailView.as_view(), name="detail"),
    path("diary-create/", views.AlbumPostCreateView.as_view(), name="create"),
]
