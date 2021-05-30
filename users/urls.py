from django.urls import path
from . import views


app_name = "users"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.log_out, name="logout"),
    path("login/kakao/", views.kakao_login, name="kakao-login"),
    path("login/kakao/callback/", views.kakao_callback, name="kakao-callback"),
    path("login/naver/", views.naver_login, name="naver-login"),
    path("login/naver/callback/", views.naver_callback, name="naver-callback"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("profile/<int:pk>/", views.UserProfileView.as_view(), name="profile"),
    path("write-list/<int:pk>", views.WritePostView.as_view(), name="write-list"),
    path("profile/update/", views.UpdateProfileView.as_view(), name="update-profile"),
    path(
        "profile/update-password/",
        views.UpdatePasswordView.as_view(),
        name="update-password",
    ),
    # path("send_email/", views.send_email, name="send_email"),
]
