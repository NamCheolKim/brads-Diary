from django import forms
from . import models


class AlbumPostCreateForm(forms.ModelForm):
    class Meta:
        model = models.PostDiary
        fields = ("title", "content", "image")

    def save(self, *args, **kwargs):
        diary = super().save(commit=False)
        return diary
