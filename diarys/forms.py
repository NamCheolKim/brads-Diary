from django import forms
from . import models

from django_summernote.widgets import SummernoteWidget


class DiaryForm(forms.ModelForm):
    class Meta:
        model = models.PostDiary
        fields = ("title", "content", "photo")
        labels = {
            "title": "제목",
            "content": "내용",
            "photo": "썸네일",
        }
        widgets = {"content": SummernoteWidget()}

    def save(self, *args, **kwargs):
        diary = super().save(commit=False)
        return diary
