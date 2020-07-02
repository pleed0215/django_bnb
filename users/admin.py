from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# Register your models here.
@admin.register(models.User)
# class CustomUserAdmin(admin.ModelAdmin):
#
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "language",
        "currency",
        "gender",
        "language",
        "avatar",
        "currency",
        "is_superhost",
    )

    list_filter = ("is_superhost", "language", "currency")
    # default UserAmdin.fieldsets + CustomFieldSets
    fieldsets = UserAdmin.fieldsets + (
        (
            "User Informations",
            {
                "fields": (
                    "gender",
                    "language",
                    "currency",
                    "is_superhost",
                    "birthday",
                    "bio",
                ),
            },
        ),
    )
