from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.log_out, name="logout")
]
