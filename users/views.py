import os
import requests
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import FormView, DetailView, TemplateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from django.core.files.base import ContentFile
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages.views import SuccessMessageMixin
from . import models, forms, mixins


class LoginView(mixins.LoggedOutOnlyView, FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("diarys:list")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        messages.success(self.request, f"어서오시개 {user.first_name}")
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("diarys:list")


def log_out(request):
    messages.info(request, f"또 오시개")
    logout(request)
    return redirect(reverse("diarys:list"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("diarys:list")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        messages.success(self.request, f"환영한다냥 {user.first_name}")
        return super().form_valid(form)


def kakao_login(request):
    client_id = os.environ.get("KAKAO_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException("Can't get authorization code.")
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        email = profile_json.get("kakao_account", None).get("email")
        if email is None:
            raise KakaoException("Please also give me your email")
        properties = profile_json.get("properties")
        nickname = properties.get("nickname")
        profile_image = properties.get("profile_image")
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException(f"Please log in with: {user.login_method}")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
            )
            user.set_unusable_password()
            user.save()
            if profile_image is not None:
                photo_request = requests.get(profile_image)
                user.avatar.save(
                    f"{nickname}-avatar", ContentFile(photo_request.content)
                )
        messages.success(request, f"어서오시개 {user.first_name}")
        login(request, user)
        return redirect(reverse("diarys:list"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


def naver_login(request):
    client_id = os.environ.get("NAVER_ID")
    state = ""
    redirect_uri = "http://127.0.0.1:8000/users/login/naver/callback"
    return redirect(
        f"https://nid.naver.com/oauth2.0/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&state={state}"
    )


class NaverException(Exception):
    pass


def naver_callback(request):
    try:
        client_id = os.environ.get("NAVER_ID")
        client_secret = os.environ.get("NAVER_SECRET")
        code = request.GET.get("code", None)
        state = request.GET.get("state", None)
        token_request = requests.get(
            f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}&state={state}"
        )
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise NaverException("Can't get authorization code.")
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://openapi.naver.com/v1/nid/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        email = profile_json.get("response", None).get("email")
        if email is None:
            raise NaverException("Please also give me your email")
        properties = profile_json.get("response")
        name = properties.get("name")
        nickname = properties.get("nickname")
        profile_image = properties.get("profile_image")
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_NAVER:
                raise NaverException(f"Please log in with: {user.login_method}")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                last_name=name,
                login_method=models.User.LOGIN_NAVER,
            )
            user.set_unusable_password()
            user.save()
            if profile_image is not None:
                photo_request = requests.get(profile_image)
                user.avatar.save(
                    f"{nickname}-avatar", ContentFile(photo_request.content)
                )
        messages.success(request, f"어서오시개 {user.first_name}")
        login(request, user)
        return redirect(reverse("diarys:list"))
    except NaverException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):
    model = models.User
    context_object_name = "user_obj"


class WritePostView(TemplateView):
    template_name = "users/wirte_post_view.html"


class UpdateProfileView(UpdateView):
    model = models.User
    template_name = "users/update-profile.html"
    fields = ("first_name", "avatar")

    def get_object(self, queryset=None):
        return self.request.user


class UpdatePasswordView(mixins.EmailLoginOnlyView, mixins.LoggedInOnlyView, SuccessMessageMixin, PasswordChangeView):
    template_name = "users/update-password.html"
    success_message = "비밀번호가 변경 되었습니다."

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "비밀번호"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "새로운 비밀번호"}
        form.fields["new_password2"].widget.attrs = {
            "placeholder": "새로운 비밀번호 확인"
        }
        return form
    
    def get_success_url(self):
        return self.request.user.get_absolute_url()
