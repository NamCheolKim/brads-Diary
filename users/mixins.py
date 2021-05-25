from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class EmailLoginOnlyView(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.login_method == "email"

    def handle_no_permission(self):
        messages.error(self.request, "비정상적인 경로로 접근하였습니다.")
        return redirect("diarys:list")


class LoggedOutOnlyView(UserPassesTestMixin):

    permission_denied_message = "Page not found"

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, "비정상적인 경로로 접근하였습니다.")
        return redirect("diarys:list")


class LoggedInOnlyView(LoginRequiredMixin):
    login_url = reverse_lazy("users:login")
