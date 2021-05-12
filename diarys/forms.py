from django import forms
from . import models

from django_summernote.widgets import SummernoteWidget


class AlbumPostCreateForm(forms.ModelForm):
    class Meta:
        model = models.PostDiary
        fields = ("title", "content")
        widgets = {"content": SummernoteWidget()}

    def save(self, *args, **kwargs):
        diary = super().save(commit=False)
        return diary
