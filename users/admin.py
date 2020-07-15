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
        "currency",
        "is_superhost",
        "is_staff",
        "email_verified",
        "login_method",
    )

    list_filter = ("is_superhost", "language", "currency", "is_superuser", "is_staff")
    # default UserAmdin.fieldsets + CustomFieldSets
    fieldsets = UserAdmin.fieldsets + (
        (
            "User Informations",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "language",
                    "currency",
                    "is_superhost",
                    "birthday",
                    "bio",
                    "login_method",
                ),
            },
        ),
    )
