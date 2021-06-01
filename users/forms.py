from django.contrib.auth.hashers import check_password
from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.CharField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "이메일"})
    )
    email.label = "이메일"
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "비밀번호"}
        )
    )
    password.label = "비밀번호"

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("비밀번호가 틀립니다."))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("이메일을 확인해 주세요."))


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("email", "first_name", "last_name")
        labels = {"email": "이메일", "last_name": "이름", "first_name": "별명"}
        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "이메일"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "별명"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "이름"}
            ),
        }

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "비밀번호"}
        )
    )
    password.label = "비밀번호"

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "비밀번호 확인"}
        )
    )
    password1.label = "비밀번호 확인"

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("이미 사용중인 이메일 입니다.", code="existing_user")
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        else:
            return password

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        try:
            models.User.objects.get(first_name=first_name)
            raise forms.ValidationError("이미 사용중인 별명입니다.", code="existing_user")
        except models.User.DoesNotExist:
            return first_name

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()


class CheckPasswordForm(forms.Form):
    password = forms.CharField(
        label="비밀번호",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "비밀번호",
            }
        ),
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = self.user.password

        if password:
            if not check_password(password, confirm_password):
                self.add_error("password", "비밀번호가 일치하지 않습니다.")
