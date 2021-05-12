from django.urls import path
from . import views


app_name = "users"

urlpatterns = [
    path("signin/", views.sign_in, name="signin"),
]
