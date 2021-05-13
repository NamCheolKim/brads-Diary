from django.urls import path
from . import views


app_name = "users"

urlpatterns = [
    path("sign-in/", views.sign_in, name="signin"),
]
