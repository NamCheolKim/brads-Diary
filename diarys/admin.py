from django.contrib import admin
from django.utils.html import mark_safe
from django_summernote.admin import SummernoteModelAdmin

from . import models


class PhotoInline(admin.TabularInline):
    model = models.Photo


@admin.register(models.PostDiary)
class PostDiaryAdmin(SummernoteModelAdmin):

    """PostDiary Admin Definition"""

    inlines = (PhotoInline,)

    list_display = (
        "title",
        "created_at",
        "updated_at",
        "count_comments",
        "count_photos",
    )

    def count_comments(self, obj):
        return obj.comments.count()

    count_comments.short_description = "Comment Count"

    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "Photo Count"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """Photo Admin Definition"""

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px" src="{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"
