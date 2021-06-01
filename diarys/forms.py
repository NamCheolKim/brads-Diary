from django import forms
from . import models

from django_summernote.widgets import SummernoteWidget


class DiaryForm(forms.ModelForm):
    class Meta:
        model = models.PostDiary
        fields = ("title", "content", "photo")
        labels = {"title": "제목", "content": "내용", "photo": "썸네일"}
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "제목"}
            ),
            "content": SummernoteWidget(attrs={"class": "form-control"}),
        }

    def save(self, *args, **kwargs):
        diary = super().save(commit=False)
        return diary


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ("content",)
        labels = {"content": "댓글내용"}

    def save(self):
        comment = super().save(commit=False)
        return comment
