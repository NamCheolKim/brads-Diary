from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from . import models


@admin.register(models.PostDiary)
class PostDiaryAdmin(SummernoteModelAdmin):

    """PostDiary Admin Definition"""

    list_display = (
        "title",
        "created_at",
        "updated_at",
        "count_comments",
        "count_photos",
    )

    def count_comments(self, obj):
        return obj.comments.count()

    def count_photos(self, obj):
        return obj.photos.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """Photo Admin Definition"""

    pass
