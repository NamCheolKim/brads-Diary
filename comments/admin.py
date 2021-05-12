from django.contrib import admin
from . import models


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):

    """Comment Admin Definition"""

    list_display = [
        "user",
        "diary",
        "comment",
        "created_at",
        "updated_at",
    ]

    list_filter = ("diary",)
