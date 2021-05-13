from django.urls import path
from diarys import views as diary_views

app_name = "core"

urlpatterns = [
    path("", diary_views.index, name="index"),
]
