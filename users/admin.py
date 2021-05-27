from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """Custom User Admin Definition"""

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": ("avatar", "login_method"),
            },
        ),
    )

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "login_method",
        "avatar",
    )
