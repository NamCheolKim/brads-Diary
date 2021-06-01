from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


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
    path("delete/", views.user_delete, name="user-delete"),
    path(
        "profile/update-password/",
        views.UpdatePasswordView.as_view(),
        name="update-password",
    ),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"),
        name="password_reset",
    ),
    path(
        "password-reset-sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_sent.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_form.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
