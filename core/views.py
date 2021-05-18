from django.views import View
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms


# 대문 페이지
def index(request):
    return render(request, "diarys/index.html")


class LoginView(View):
    def get(self, request):
        form = forms.LoginForm()
        context = {"form": form}
        return render(request, "core/login.html", context)

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("diarys:list"))
        context = {"form": form}
        return render(request, "core/login.html", context)


def log_out(request):
    logout(request)
    return redirect(reverse("diarys:list"))
