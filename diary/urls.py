from django.urls import path
from . import views

app_name = "diary"

urlpatterns = [
    path("", views.index, name="index"),
    path("album/", views.unfold, name="album"),
    path("detail/", views.detail, name="detail"),
]
