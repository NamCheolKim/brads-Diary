from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from . import models


class PostDiaryAdmin(SummernoteModelAdmin):
    list_display = ("title", "created_at")


admin.site.register(models.PostDiary, PostDiaryAdmin)
