from django import forms
from . import models as user_model


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = user_model.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("비밀번호가 틀립니다."))
        except user_model.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("존재하지 않는 사용자입니다."))
